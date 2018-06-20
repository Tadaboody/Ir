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
from statistics import median_high, mean
from math import floor
from product_team import EnglishAnalyzer
from product_team.utils import memorize
from os.path import join
from product_team import SAVE_DIR

WORD2VEC_SIZE = 20


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
            (i, token) for i, token in enumerate(self.tokenized_nbest_answers) if token is not None]
        self.nbest_answers = [self.nbest_answers[i]
                              for i, _ in self.tokenized_nbest_answers]

    @property
    def tokenized_fields(self):
        if self.tokenized_question is not None:
            yield self.tokenized_question
        yield from self.tokenized_answers

    @property
    def tokenized_answers(self):
        if self.tokenized_best_answer:
            yield self.tokenized_best_answer
        for _, answer in self.tokenized_nbest_answers:
            yield answer

    # @property
    # def answer_pairs(self) -> Tuple(str,List[str]):
    #     if self.tokenized_best_answer:
    #         yield self.best_answer, self.tokenized_best_answer
    #     for answer in self.nbest_answers:
    #         tokenized_answer = global_analay.tokenize(answer)


class Index:
    class Corpus_iterator:  # Word2Vec receives an iterator
        def __init__(self, index):
            self.index = index

        def __iter__(self):
            yield from self.index.gen_corpus()

    def gen_corpus(self):
        for doc in self.doclist:
            for sentence in doc.tokenized_fields:
                yield sentence

    def max_sentence_length(self):
        return max(self.sentance_length_array)

    def __init__(self, dataset_path=join("dataset", "nfL6.json"), Word2Vec_path=join(SAVE_DIR, "word2vec"), doclist_path=join(SAVE_DIR, "doclist.p")):
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
            self.doclist, test_size=0.1)

    @lazy
    def normalize_vector_length(self):
        return self.average_sentance_length()

    @lazy
    def sentance_length_array(self):
        return [len(sentance) for sentance in self.Corpus_iterator(self)]

    def median_vector_length(self):
        return median_high(self.sentance_length_array)

    def average_sentance_length(self):
        return floor(mean(self.sentance_length_array))

    @lazy
    def test_size(self):
        return sum(len(list(doc.tokenized_answers)) for doc in self.doc_test)

    def process_for_train(self, text: str):
        tokens = self.analyzer.tokenize(text)
        if not tokens:
            return None
        vector = self.model[tokens]
        if len(vector) < self.normalize_vector_length:
            vector = np.append(vector, [np.zeros(WORD2VEC_SIZE)
                                        for _ in range(self.normalize_vector_length - len(vector))], axis=0)
        vector = vector[:self.normalize_vector_length]
        return vector

    def generate_batch(self, batch_size):
        def random_answer():
            random_doc = random.choice(self.doc_train)  # type:Document
            return random.choice(list(random_doc.tokenized_answers))

        def doc_iterator():
            for doc in self.doc_train:
                for answer in doc.tokenized_answers:
                    yield self.process_for_train(answer), self.process_for_train(doc.tokenized_question), self.process_for_train(random_answer())

        generator = doc_iterator()
        for _ in range(self.test_size//batch_size):
            ret = list(zip(*islice(generator, batch_size)))
            yield np.array(ret)


def load_index():
    return Index()
