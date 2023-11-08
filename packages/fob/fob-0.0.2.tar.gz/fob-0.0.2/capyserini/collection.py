import json
import logging
import os

from functools import cache, cached_property
from typing import List, Type

import ir_datasets
import numpy as np
import optuna

from trecrun import TRECRun

from fob import cacheable, configurable, Ingredient
from fob.cli import config_dict_to_string, config_string_to_dict
from fob.serialize import NumpyOutput, PathOutput, RunOutput

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

THREADS = 8  # LTODO

DEFAULT_METRICS = [
    "P@1",
    "P@5",
    "P@10",
    "P@20",
    "P@30",
    "Judged@10",
    "Judged@20",
    "Judged@50",
    "AP@100",
    "AP@1000",
    "nDCG@5",
    "nDCG@10",
    "nDCG@20",
    "Recall@100",
    "Recall@1000",
    "RR",
]


class Collection(Ingredient):
    def __iter__(self):
        raise NotImplementedError()

    @cacheable(PathOutput)
    def as_path(self, tmp_path_context=None, MAX_THREADS=128):
        with tmp_path_context() as path:
            os.makedirs(path)
            fns = [open(path / f"{i}.json", "wt", encoding="utf-8") for i in range(MAX_THREADS)]
            for i, doc in enumerate(self):
                fn = fns[i % MAX_THREADS]
                print(json.dumps(doc), file=fn)

            for fn in fns:
                fn.close()

        return path

    # LTODO ? validate document path
    # find document path (downloading if necessary)


class IRDSCollection(Collection):
    @configurable
    def __init__(self, name: str = "disks45/nocr/trec-robust-2004"):
        pass

    @cached_property
    def dataset(self):
        import ir_datasets

        return ir_datasets.load(self.cfg["name"])

    @cached_property
    def docs_store(self):
        return self.dataset.docs_store()

    def warm(self):
        super().warm()

        # load cached properties
        self.dataset
        for _ in self.docs_store:
            break

    def __iter__(self):
        for doc in self.docs_store:
            yield self.doc_as_json(doc)

    def doc_as_json(self, doc):
        # LTODO is body always the only field? title??
        return {"id": doc.doc_id, "contents": doc.body}


class PyseriniIndexCollection(Collection):
    @configurable
    def __init__(self, name: str = "robust04"):
        pass

    @cached_property
    def reader(self):
        from pyserini.index.lucene import IndexReader

        return IndexReader.from_prebuilt_index(self.cfg["name"])

    @cached_property
    def searcher(self):
        from pyserini.search.lucene import LuceneSearcher

        return LuceneSearcher.from_prebuilt_index(self.cfg["name"])

    def warm(self):
        super().warm()
        # load cached properties
        self.reader
        self.searcher.num_docs

    def __iter__(self):
        for i in range(self.searcher.num_docs):
            yield self.doc_as_json(self.searcher.doc(i))

    def doc_as_json(self, doc):
        return {"id": doc.docid(), "contents": doc.raw()}


class AnseriniIndex(Ingredient):
    @configurable
    def __init__(
        self,
        collection: Type[Collection] = IRDSCollection(),
        stemmer: str = None,
        filter_stopwords: bool = False,
        store_positions: bool = True,
        store_docvectors: bool = True,
    ):
        pass

    def warm(self):
        super().warm()
        # load cached properties
        self.index_path

    @cacheable(PathOutput)
    def index_path(self, MAX_THREADS=8, tmp_path_context=None):
        from pyserini.index.lucene import IndexReader  # this import makes pyserini add anserini's fatjar to the classpath
        from jnius import autoclass

        with tmp_path_context() as output_path:
            output_path = output_path.as_posix()
            os.makedirs(output_path)

            collection_path = self.cfg["collection"].as_path()
            if not os.path.exists(collection_path):
                raise RuntimeError(f"collection_path does not exist: {collection_path}")

            JIndexCollection = autoclass("io.anserini.index.IndexCollection")
            args = [
                "-collection",
                "JsonCollection",
                "-generator",
                "DefaultLuceneDocumentGenerator",
                "-threads",
                str(MAX_THREADS),
                "-input",
                collection_path,
                "-index",
                output_path,
                "-stemmer",
                self.cfg["stemmer"] if self.cfg["stemmer"] else "none",
            ]

            if not self.cfg["filter_stopwords"]:
                args.append("-keepStopwords")
            if self.cfg["store_positions"]:
                args.append("-storePositions")
            if self.cfg["store_docvectors"]:
                args.append("-storeDocvectors")

            JIndexCollection.main(args)

        print("----------------------\nmade some index:", output_path)
        print(IndexReader(output_path).stats())

        stats = IndexReader(output_path).stats()
        if stats["documents"] < 1:
            raise RuntimeError(f"indexing seems to have failed (no documents): {stats}")

        return output_path

    @cached_property
    def reader(self):
        from pyserini.index.lucene import IndexReader

        return IndexReader(self.index_path())

    @cached_property
    def tokenizer(self):
        from tokenizer import PyseriniAnalyzer

        return PyseriniAnalyzer(stemmer=self.cfg["stemmer"], filter_stopwords=self.cfg["filter_stopwords"])

    def term_iter(self):
        for term in self.reader.terms():
            yield term

    def term_counts(self, term, tokenize=True):
        analyzer = self.tokenizer.analyzer.analyzer if tokenize else None
        return self.reader.get_term_counts(term, analyzer=analyzer)

    def term_postings_list(self, term, tokenize=True):
        analyzer = self.tokenizer.analyzer.analyzer if tokenize else None
        return self.reader.get_postings_list(term, analyzer=analyzer)


class PyseriniSearcher(Ingredient):
    @cached_property
    def tokenizer(self):
        from tokenizer import PyseriniAnalyzer

        return PyseriniAnalyzer(
            stemmer=self.cfg["index"].cfg["stemmer"], filter_stopwords=self.cfg["index"].cfg["filter_stopwords"]
        )

    @cached_property
    def searcher(self):
        from pyserini.search.lucene import LuceneSearcher

        searcher = LuceneSearcher(self.cfg["index"].index_path())
        self.searcher_set(searcher)

        if self.cfg.get("expansion", None) is not None:
            self.cfg["expansion"].set(searcher)

        if self.cfg.get("sdm", None) is not None:
            self.query_generator = self.cfg["sdm"].query_generator
        else:
            self.query_generator = None

        searcher.set_analyzer(self.tokenizer.analyzer.analyzer)

        return searcher

    def warm(self):
        super().warm()
        # load cached properties
        self.searcher

    def hits_to_dict(self, hits):
        return {hit.docid: hit.score for hit in hits}

    def search(self, query, k: int = 10):
        hits = self.searcher.search(query, k=k, query_generator=self.query_generator)
        return self.hits_to_dict(hits)

    @cacheable(RunOutput)
    def batch_search(self, queries: dict, k: int = 10):
        qids, queries = zip(*queries.items())

        qid_hits = self.searcher.batch_search(
            queries=queries, qids=qids, k=k, threads=THREADS, query_generator=self.query_generator
        )
        return TRECRun({qid: self.hits_to_dict(hits) for qid, hits in qid_hits.items()})

    @cacheable(RunOutput)
    def batch_searchcollection(self, queries: dict, k: int = 10, tmp_path_context=None):
        from pyserini.pyclass import autoclass

        SearchCollection = autoclass("io.anserini.search.SearchCollection")

        with tmp_path_context() as tmp_path:
            os.makedirs(tmp_path)
            topicsfn = (tmp_path / "topics.tsv").as_posix()
            outputfn = (tmp_path / "results.run").as_posix()

            with open(topicsfn, "wt", encoding="utf-8") as outf:
                for qid, query in queries.items():
                    print(f"{qid}\t{self.tokenize_query(query)}", file=outf)

            args = [
                "-topicreader",
                "TsvString",
                "-index",
                self.cfg["index"].index_path(),
                "-topics",
                topicsfn,
                "-output",
                outputfn,
                "-inmem",
                "-threads",
                str(THREADS),
                "-stemmer",
                self.cfg["index"]["stemmer"] if self.cfg["index"]["stemmer"] else "none",
                "-hits",
                str(k),
            ]

            if not self.cfg["index"]["filter_stopwords"]:
                args.append("-keepstopwords")

            args.extend(self.search_args)
            if self.cfg["expansion"]:
                args.extend(self.cfg["expansion"].search_args)

            if self.cfg["sdm"]:
                args.extend(self.cfg["sdm"].search_args)

            SearchCollection.main(args)
            run = TRECRun(outputfn)

        return run


class IRDSBenchmark(Ingredient):
    # LTODO the annotations for train/dev/test here should indicate a list, but this resulted in them being moved to dep.
    @configurable
    def __init__(
        self,
        name: str = "disks45/nocr/trec-robust-2004",
        train: List[str] = ["fold1", "fold2", "fold3"],
        dev: List[str] = ["fold4"],
        test: List[str] = ["fold5"],
        query_type: str = "title",
    ):
        # query_type is title/description/narrative for robust04 or 'text' for msmarco
        # relevance_level for binary metrics?
        pass

    @cached_property
    def dataset(self):
        return ir_datasets.load(self.cfg["name"])

    @staticmethod
    def dataset_qrels(dataset):
        qrels = {}
        for qrel in dataset.qrels_iter():
            qrels.setdefault(qrel.query_id, {})
            qrels[qrel.query_id][qrel.doc_id] = max(qrel.relevance, qrels[qrel.query_id].get(qrel.doc_id, -999))
        return qrels

    @staticmethod
    def dataset_queries(dataset, query_type):
        topics = {}
        for query in dataset.queries_iter():
            topics[query.query_id] = getattr(query, query_type)
        return topics

    @cached_property
    def qrels(self):
        return self.dataset_qrels(ir_datasets.load(self.cfg["name"]))

    @cached_property
    def queries(self):
        return self.dataset_queries(ir_datasets.load(self.cfg["name"]), self.cfg["query_type"])

    @cache
    def split_qrels(self, split):
        # LTODO validate: remove empty qrels?
        if split not in self.cfg:
            raise ValueError(f"split={split} not found in self.cfg; typically split is in (train, dev, test)")

        qrels = {}
        for foldname in self.cfg[split]:
            ds = ir_datasets.load(self.cfg["name"] + "/" + foldname)
            qrels.update(self.dataset_qrels(ds))
        return qrels

    @cache
    def split_queries(self, split):
        # LTODO validate: have text for qid+type in each fold
        if split not in self.cfg:
            raise ValueError(f"split={split} not found in self.cfg; typically split is in (train, dev, test)")

        topics = {}
        for foldname in self.cfg[split]:
            ds = ir_datasets.load(self.cfg["name"] + "/" + foldname)
            topics.update(self.dataset_queries(ds, self.cfg["query_type"]))
        return topics

    def all_folds(self):
        basename = self.cfg["name"][:-1]
        candidates = [f"fold{idx}" for idx in range(11)]
        folds = [x for x in candidates if f"{self.cfg['name']}/{x}" in ir_datasets.registry]
        assert len(folds) > 0
        return folds

    def all_splits(self):
        base_cfg = {k: v for k, v in self.cfg.items() if k not in ("train", "dev", "test")}

        splits = []
        folds = self.all_folds()
        for testidx, testfold in enumerate(folds):
            if testidx == 0:
                devidx = len(folds) - 1
            else:
                devidx = testidx - 1
            devfold = folds[devidx]
            trainfolds = [k for k in folds if k != testfold and k != devfold]

            split_cfg = {k: v for k, v in base_cfg.items() if k != "__name"}
            split_cfg["train"] = trainfolds
            split_cfg["dev"] = [devfold]
            split_cfg["test"] = [testfold]

            split_benchmark = IRDSBenchmark(**split_cfg)
            split_benchmark.caching_like(self)
            splits.append(split_benchmark)

        return splits


class PyseriniBM25(PyseriniSearcher):
    @configurable
    def __init__(
        self,
        index: Type[Ingredient] = AnseriniIndex(),
        expansion: Type[Ingredient] = None,
        sdm: Type[Ingredient] = None,
        k1: float = 0.9,
        b: float = 0.4,
    ):
        self.searcher_set = lambda x: x.set_bm25(k1=k1, b=b)
        self.search_args = f"-bm25 -bm25.b {b} -bm25.k1 {k1}".split()

    def optuna_suggest(self, trial, prefix=""):
        cfg = {}
        trial.suggest_categorical(prefix + "__name", (self.name,))
        cfg["k1"] = trial.suggest_float(prefix + "k1", 0.01, 100, log=True)
        cfg["b"] = trial.suggest_float(prefix + "b", 0, 1, step=0.01)
        cfg["index"] = self.cfg["index"]  # LTODO optuna_suggest
        cfg["expansion"] = self.cfg["expansion"].optuna_suggest(trial, prefix="expansion.") if self.cfg["expansion"] else None
        cfg["sdm"] = self.cfg["sdm"].optuna_suggest(trial, prefix="sdm.") if self.cfg["sdm"] else None
        obj = self.__class__(**cfg)
        obj.caching_like(self)
        return obj


class PyseriniQL(PyseriniSearcher):
    @configurable
    def __init__(
        self,
        index: Type[Ingredient] = AnseriniIndex(),
        expansion: Type[Ingredient] = None,
        sdm: Type[Ingredient] = None,
        mu: float = 1000,
    ):
        self.searcher_set = lambda x: x.set_qld(mu=mu)
        self.search_args = f"-qld -qld.mu {mu}".split()

    def optuna_suggest(self, trial, prefix=""):
        cfg = {}
        trial.suggest_categorical(prefix + "__name", (self.name,))
        cfg["mu"] = trial.suggest_int("mu", 1, 100000)
        cfg["index"] = self.cfg["index"]  # LTODO optuna_suggest
        cfg["expansion"] = self.cfg["expansion"].optuna_suggest(trial, prefix="expansion.") if self.cfg["expansion"] else None
        cfg["sdm"] = self.cfg["sdm"].optuna_suggest(trial, prefix="sdm.") if self.cfg["sdm"] else None
        obj = self.__class__(**cfg)
        obj.caching_like(self)
        return obj


class PyseriniRM3(Ingredient):
    @configurable
    def __init__(
        self, fb_terms: int = 10, fb_docs: int = 10, original_query_weight: float = 0.5, filter_nonenglish_terms: bool = True
    ):
        self.search_args = (
            f"-rm3 -rm3.fbTerms {fb_terms} -rm3.fbDocs {fb_docs} -rm3.originalQueryWeight {original_query_weight}".split()
        )

        if not filter_nonenglish_terms:
            self.search_args.append("-rm3.noTermFilter")  # turn off English term filter

    def optuna_suggest(self, trial, prefix=""):
        cfg = {}
        trial.suggest_categorical(prefix + "__name", (self.name,))
        cfg["fb_terms"] = trial.suggest_int(prefix + "fb_terms", 1, 1000, log=True)
        cfg["fb_docs"] = trial.suggest_int(prefix + "fb_docs", 1, 1000, log=True)
        cfg["original_query_weight"] = trial.suggest_float(prefix + "original_query_weight", 0.01, 1, step=0.01)
        obj = self.__class__(**cfg)
        obj.caching_like(self)
        return obj

    def set(self, searcher):
        searcher.set_rm3(
            fb_terms=self.cfg["fb_terms"],
            fb_docs=self.cfg["fb_docs"],
            original_query_weight=self.cfg["original_query_weight"],
            filter_terms=self.cfg["filter_nonenglish_terms"],
        )


class PyseriniSDM(Ingredient):
    @configurable
    def __init__(self, term_weight: float = 0.85, ordered_window_weight: float = 0.1, unordered_window_weight: float = 0.05):
        self.search_args = f"-sdm -sdm.tw {term_weight} -sdm.ow {ordered_window_weight} -sdm.uw {unordered_window_weight}".split()

    def optuna_suggest(self, trial, prefix=""):
        cfg = {}
        trial.suggest_categorical(prefix + "__name", (self.name,))
        cfg["term_weight"] = trial.suggest_float(prefix + "term_weight", 0, 1, step=0.01)
        cfg["ordered_window_weight"] = trial.suggest_float(prefix + "ordered_window_weight", 0, 1, step=0.01)
        cfg["unordered_window_weight"] = trial.suggest_float(prefix + "unordered_window_weight", 0, 1, step=0.01)
        obj = self.__class__(**cfg)
        obj.caching_like(self)
        return obj

    @cached_property
    def query_generator(self):
        from jnius import autoclass

        JSDMQueryGenerator = autoclass("io.anserini.search.query.SdmQueryGenerator")
        return JSDMQueryGenerator(self.cfg["term_weight"], self.cfg["ordered_window_weight"], self.cfg["unordered_window_weight"])


class OptunaSearcher(Ingredient):
    @configurable
    def __init__(
        self,
        trials: int = 100,
        searcher: Type[Ingredient] = PyseriniBM25(),
        train_benchmark: Type[Ingredient] = IRDSBenchmark(),
        optimize: str = "AP@1000",
        direction: str = "maximize",
        train_k: int = 100,
        eval_k: int = 100,
    ):
        pass

    def _objective(self, trial):
        new_searcher = self.cfg["searcher"].optuna_suggest(trial, prefix="")
        assert self.cfg["optimize"] in DEFAULT_METRICS, "LTODO make configurable"
        pipeline = BenchmarkSearcher(
            searcher=new_searcher, benchmark=self.cfg["train_benchmark"], k=self.cfg["train_k"], split="train"
        )
        metrics = pipeline.main()
        return metrics[self.cfg["optimize"]]["mean"]

    @cached_property
    def study(self):
        opt_study = optuna.create_study(directions=[self.cfg["direction"]], sampler=optuna.samplers.TPESampler(seed=42))
        opt_study.optimize(self._objective, n_trials=self.cfg["trials"])
        return opt_study

    @cached_property
    def best_config(self):
        return config_string_to_dict(config_dict_to_string(self.study.best_params))

    @cached_property
    def tuned_searcher(self):
        from fob.base import instantiate_object

        cfg = self.best_config
        return instantiate_object(cfg, search_path=self.cfg["searcher"].search_path, output_path=self.cfg["searcher"].output_path)

    def main(self):
        print("best_params:", self.study.best_params)
        print(self.study.trials_dataframe())
        print(self.tuned_searcher)

    ###
    def search(self, query, k: int = 10):
        pass

    @cacheable(RunOutput)
    def batch_search(self, queries: dict, k: int = 10):
        pass

    @cacheable(RunOutput)
    def batch_searchcollection(self, queries: dict, k: int = 10, tmp_path_context=None):
        pass


class BenchmarkSearcher(Ingredient):
    @configurable
    def __init__(
        self,
        searcher: Type[Ingredient] = PyseriniBM25(),
        benchmark: Type[Ingredient] = IRDSBenchmark(),
        metrics: str = "default",
        k: int = 100,
        split: str = "test",
    ):
        pass

    def all_results(self):
        base_cfg = {k: v for k, v in self.cfg.items() if k != "__name"}
        base_cfg["searcher"] = self.cfg["searcher"]

        split_results = []
        for benchmark in self.cfg["benchmark"].all_splits():
            base_cfg["benchmark"] = benchmark
            bs = BenchmarkSearcher(**base_cfg)
            bs.caching_like(self)
            split_results.append(bs.main())

        combined_results = {}
        for split in split_results:
            for metric in split:
                for qid in split[metric]:
                    if qid != "mean":
                        assert qid not in combined_results.get(metric, {}), "unsupported: same qid appears in multiple splits"
                        combined_results.setdefault(metric, {})[qid] = split[metric][qid]

        avg_metrics = {metric: np.mean(list(combined_results[metric].values())) for metric in combined_results}
        logger.info("cross-validated results:")
        for metric, score in sorted(avg_metrics.items()):
            logger.info("%25s: %0.4f", metric, score)

        return avg_metrics

    def searcher_run(self):
        queries = self.cfg["benchmark"].split_queries(self.cfg["split"])
        return self.cfg["searcher"].batch_search(queries, k=self.cfg["k"])  # , _exec="python -m fob.base")
        # return self.cfg["searcher"].batch_searchcollection(queries, k=self.cfg["k"])

    def main(self):
        qrels = self.cfg["benchmark"].split_qrels(self.cfg["split"])

        trecrun = self.searcher_run()
        assert self.cfg["metrics"] == "default"
        metrics = DEFAULT_METRICS
        results = trecrun.evaluate(qrels, metrics)
        # results is qid -> metric -> value
        # print("BenchmarkSearcher results: %s" % results)

        return results

    def ttest(self, anint: int = 1, afloat: float = 2.0, somestr: str = "bar", george: bool = True):
        print(type(anint), anint)
        print(type(afloat), afloat)
        print(type(somestr), somestr)
        print(type(george), george)


# TODO test BEIR with irds
