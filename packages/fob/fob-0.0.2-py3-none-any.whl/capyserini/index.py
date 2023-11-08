from fob import Ingredient


class InvertedIndex(Ingredient):
    pass


from pyserini.search.lucene import LuceneSearcher

LuceneSearcher.list_prebuilt_indexes()
