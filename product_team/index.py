""" Module for basic searcher classes"""
import json
import pickle
import random
from collections import namedtuple
from itertools import islice
from typing import Iterator, List, Tuple

import numpy as np
from gensim.corpora import Dictionary
from gensim.models import TfidfModel, Word2Vec
from gensim.similarities import SparseMatrixSimilarity
from lazy import lazy
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from product_team import EnglishAnalyzer
from product_team.utils import memorize

WORD2VEC_SIZE = 100


class Document:
    def __init__(self, question, best_answer, nbest_answers, analyzer: EnglishAnalyzer):
        self.question = question
        self.best_answer = best_answer
        self.nbest_answers = [
            answer for answer in nbest_answers if answer != best_answer]
        self.tokenize(analyzer)

    def tokenize(self, analyzer: EnglishAnalyzer):
        self.tokenized_question = analyzer.tokenize(self.question)
        self.tokenized_best_answer = analyzer.tokenize(self.best_answer)
        self.tokenized_nbest_answers = [analyzer.tokenize(answer)
                                        for answer in self.nbest_answers]
        self.tokenized_nbest_answers = [
            token for token in self.tokenized_nbest_answers if token is not None]

    @property
    def tokenized_fields(self):
        yield self.tokenized_question
        if self.tokenized_best_answer:
            yield self.tokenized_best_answer
        for answer in self.tokenized_nbest_answers:
            yield answer


class Index:
    class Corpus_iterator:  # Word2Vec receives an iterator
        def __init__(self, index):
            self.index = index

        def __iter__(self):
            for sentence in self.index.gen_corpus():
                yield sentence

    def gen_corpus(self):
        for doc in self.doclist:
            for sentence in doc.tokenized_fields:
                yield sentence
    
    @lazy
    def max_sentence_length(self):
        return len(max(self.Corpus_iterator(self), key=lambda sent: len(sent)))

    def __init__(self, dataset_path="dataset/nfL6.json", Word2Vec_path="word2vec", doclist_path="doclist.p"):
        self.analyzer = EnglishAnalyzer()
        try:
            with open(doclist_path, 'rb') as fp:
                self.doclist = pickle.load(fp)
        except FileNotFoundError:
            with open(dataset_path) as fp:
                dataset = json.load(fp)
                self.doclist = [
                    Document(data['question'], data['answer'],
                             data['nbestanswers'], self.analyzer)
                    for data in tqdm(dataset)]
            with open(doclist_path, 'wb') as fp:
                pickle.dump(self.doclist, fp)

        self.doclist = [
            doc for doc in self.doclist if doc.tokenized_question is not None]
        try:
            self.model = Word2Vec.load(Word2Vec_path)
        except FileNotFoundError:
            self.model = Word2Vec(
                Index.Corpus_iterator(self), size=WORD2VEC_SIZE, min_count=1)
            self.model.save(Word2Vec_path)
        self.doc_train, self.doc_test = train_test_split(
            self.doclist, test_size=0.2)

    def process_for_train(self, text: str):
        tokens = self.analyzer.tokenize(text)
        return self.model[tokens]

    def generate_batch(self, batch_size):
        def random_answer():
            random_doc = random.choice(self.doc_train)  # Type:Document
            return random.choice(random_doc.tokenized_nbest_answers + random_doc.tokenized_best_answer)

        def doc_iterator():
            for doc in self.doc_train:
                for answer in doc.tokenized_nbest_answers + doc.tokenized_best_answer:
                    yield self.model[answer], self.model[doc.tokenized_question], self.model[random_answer()]

        generator = doc_iterator()
        while True:
            ret = list(zip(*islice(generator, 30)))
            if ret:
                yield np.array(ret)
            else:
                return

    def search(self, query: str):
        ...


def load_index():
    return Index()
