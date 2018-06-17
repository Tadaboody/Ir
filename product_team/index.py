""" Module for basic searcher classes"""
import json
from collections import namedtuple
from typing import Iterator

from gensim.corpora import Dictionary
from gensim.models import TfidfModel, Word2Vec
from gensim.similarities import SparseMatrixSimilarity
from lazy import lazy
from tqdm import tqdm

from product_team import EnglishAnalyzer
from product_team.utils import memorize

Question = namedtuple(
    'Question', ['id','question', 'nbestanswers', 'answer', 'main_category'])
Answer = namedtuple('Answer',['id','answers'])


class Index:
    """ Base class for an searcher of questions"""

    def __init__(self, path: str):
        self.documents = dict()  # List[Question]
        self.indexed_documents = list()
        self.raw_answers = list()
        self.index_file(path)
    
    @lazy
    def analyzer(self):
        return EnglishAnalyzer()

    def index_file(self, path: str): # -> Index
        """ Initialization method for creating an searcher from a json"""
        CACHE_PATH = path + 'analyzed_answers.json'
        try:
            with open(CACHE_PATH) as fp:
                self.indexed_documents, self.raw_answers = json.load(fp)
        except FileNotFoundError:
            with open(path) as fp:
                question_list = json.load(fp)
            for question in tqdm(question_list):
                self.add_doc(Question(**question))
            with open(CACHE_PATH,'w') as fp:
                json.dump([self.indexed_documents, self.raw_answers], fp)
        self.fit()

    def add_doc(self, question: Question):
        """ Indexes a single question """
        self.documents[question.id] = question
        for answer in question.nbestanswers:
            self.indexed_documents.append(self.analyzer.tokenize(answer))
            self.raw_answers.append(answer)

    def fit(self):
        """ Generate the searcher and its model, has to be called before vectorize and search"""
        dataset = list(self.all_answers)
        dct = Dictionary(dataset)
        self.corpus = [dct.doc2bow(line) for line in dataset]
        self.model = TfidfModel(self.corpus)
    
    def vectorize(self, doc: str):
        return self.model[doc]
    
    @lazy
    def searcher(self):
        return SparseMatrixSimilarity(self.vectorize(self.corpus))

    def search(self, doc, nbest=5):
        top_docs_indicies = sorted(
            self.searcher[self.vectorize(doc)], key=lambda vec: vec[1])
        top_docs_indicies = list(top_docs_indicies)[:nbest]
        top_docs_indicies = [top_doc[0] for top_doc in top_docs_indicies]
        return [self.raw_answers[index] for index in top_docs_indicies]

    @property
    def all_answers(self) -> Iterator[str]:
        return self.indexed_documents

def load_index():
    return Index("dataset/nfL6.json")
