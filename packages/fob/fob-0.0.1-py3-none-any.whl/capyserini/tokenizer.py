from functools import cached_property

from pyserini.analysis import Analyzer, get_lucene_analyzer

from fob import configurable, Ingredient


class Tokenizer(Ingredient):
    pass


class PyseriniAnalyzer(Tokenizer):
    @configurable
    def __init__(self, language: str = "en", stemmer: str = None, filter_stopwords: bool = False):
        pass

    @cached_property
    def analyzer(self):
        return Analyzer(
            get_lucene_analyzer(
                language=self.cfg["language"],
                stemmer=self.cfg["stemmer"],
                stemming=self.cfg["stemmer"] is not None,
                stopwords=self.cfg["filter_stopwords"],
            )
        )

    def tokenize(self, s):
        return self.analyzer.analyze(s)
