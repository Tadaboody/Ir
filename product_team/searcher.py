import pickle
from collections import namedtuple,deque
from functools import cmp_to_key
from heapq import nlargest
from itertools import islice
from os.path import join

import numpy as np
from lazy import lazy
from scipy.spatial.distance import cosine as cosine_distance
from tqdm import tqdm

from product_team import SAVE_DIR, Document, Index, run, run_multi

ModeledBestAnswer = namedtuple(
    'ModeledBestAnswer', ['index', 'answer', 'document'])


def cosine_similarity(a, b):
    return 1.0 - cosine_distance(a, b)


class SearchableDoc():
    def __init__(self, doc: Document, modeled_best_answer, modeled_nbest_answers):
        self.doc = doc
        self.modeled_nbest_answers = [ModeledBestAnswer(i, answer, doc) for (i, _), answer in zip(doc.nbest_answers, modeled_nbest_answers)]
        self.modeled_best_answer = ModeledBestAnswer(-1, modeled_best_answer, self)

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
            self.gen_model_batch()
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
            if not a.answer:
                return float('-inf')
            return cosine_similarity(query, a.answer)

        best_mod_answers = nlargest(
            n, self.all_answers, key=doc_score)

        def modeled_answer_to_answer(modeled_answer: ModeledBestAnswer):
            modeled_answer_doc = modeled_answer.document  # type:SearchableDoc
            ind = modeled_answer.index
            if ind == -1:
                return modeled_answer_doc.doc.best_answer
            else:
                return modeled_answer_doc.doc.nbest_answers[ind]

        return [{"answer": modeled_answer_to_answer(mod_answer), "score": doc_score(mod_answer)}
                for mod_answer in best_mod_answers if doc_score(mod_answer) > SIM_THRESH]

    def gen_model_batch(self):
        self.doclist = []
        print("startgen")
        lengths = deque([len(list(doc.tokenized_answers))
                   for doc in self.index.doclist])
        all_tokenized_answers = np.array(
            list(np.array(list(self.index.process_for_train(answer) for answer in doc.tokenized_answers))
            for doc in self.index.doclist))
        docs = deque(self.index.doclist)
        for batch in np.array_split(all_tokenized_answers,100):
            print("batch")
            modeled_batch = deque(run_multi(batch))
            current_length = lengths.popleft()
            current_doc = docs.popleft() #type:Document
            if current_doc.tokenized_best_answer:
                best_answer = modeled_batch.popleft()
                current_length -= 1
            nbest_answers = [modeled_batch.popleft() for _ in range(current_length)]
            self.doclist.append(SearchableDoc(
                current_doc, best_answer, nbest_answers))

