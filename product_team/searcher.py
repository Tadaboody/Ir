import pickle
from collections import namedtuple
from functools import cmp_to_key
from heapq import nlargest
from os.path import join

from lazy import lazy
from scipy.spatial.distance import cosine as cosine_distance
from tqdm import tqdm

from product_team import SAVE_DIR, Document, Index, run

ModeledBestAnswer = namedtuple(
    'ModeledBestAnswer', ['index', 'answer', 'document'])


def cosine_similarity(a, b):
    return 1.0 - cosine_distance(a, b)


class SearchableDoc():
    def __init__(self, doc: Document, index: Index):
        self.doc = doc
        self.index = index
        self.modeled_nbest_answers = [ModeledBestAnswer(i, self.process(
            answer), self) for i, answer in self.doc.tokenized_nbest_answers]
        self.modeled_best_answer = ModeledBestAnswer(
            -1, self.process(doc.tokenized_best_answer), self)

    def process(self, text: str):
        return run(self.index.process_for_train(text))

    @property
    def all_modeled_answers(self):
        yield self.modeled_best_answer
        yield from self.modeled_nbest_answers


class Searcher:
    def __init__(self, index: Index):
        self.index = index
        self.doclist_path = join(SAVE_DIR, 'searchable_doclist.p')
        try:
            with open(self.doclist_path, 'rb') as fp:
                self.doclist = pickle.load(fp)
        except FileNotFoundError:
            self.doclist = [SearchableDoc(doc, self.index)
                            for doc in tqdm(self.index.doclist)]
            with open(self.doclist_path, 'wb') as fp:
                pickle.dump(self.doclist, fp)

    @lazy
    def all_answers(self):
        for doc in self.doclist:
            yield from doc.all_modeled_answers

    def search(self, question: str, n=5):
        SIM_THRESH = 0.5
        query = run(self.index.process_for_train(question))

        def doc_score(a: ModeledBestAnswer):
            return cosine_similarity(query, a.answer)

        best_mod_answers = nlargest(
            n, self.all_answers, key=doc_score)

        def modeled_answer_to_answer(modeled_answer: ModeledBestAnswer):
            modeled_answer_doc = modeled_answer.document  # type:SearchableDoc
            ind = modeled_answer.index
            if ind == "-1":
                return modeled_answer_doc.doc.best_answer
            else:
                return modeled_answer_doc.doc.nbest_answers[ind]

        return [{"answer": modeled_answer_to_answer(mod_answer), "score": doc_score(mod_answer)}
                for mod_answer in best_mod_answers if doc_score(mod_answer) > SIM_THRESH]