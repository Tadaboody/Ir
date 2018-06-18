import json

import numpy as np
import pytest

from product_team import Index, load_index

test_question = {
    "main_category": "Business & Finance",
    "question": "What is a theopneust?",
    "nbestanswers": [
        "A \"theopneust\" is a misspelling.  The correct spelling is \"theopneusty\".",
        "The\u00b7op\u00b7neus\u00b7ty. n.. Divine inspiration; the supernatural influence of the Divine Spirit in qualifying men to receive and communicate revealed truth."
    ],
    "answer": "The\u00b7op\u00b7neus\u00b7ty. n.. Divine inspiration; the supernatural influence of the Divine Spirit in qualifying men to receive and communicate revealed truth.",
    "id": "213773"
}


@pytest.fixture(scope="session")
def index():
    return load_index()


@pytest.fixture
def question():
    return test_question['question']
# @pytest.fixture
# def index(question):
#     ret = Index('/')
#     ret.add_doc(question)
#     return ret


def test_word2vec_vocab(index: Index):
    for sentence in index.Corpus_iterator(index):
        assert index.model[sentence].shape[1] == 100


def test_batches(index: Index):
    batch_size = 30
    for _, batch_triple in zip(range(3), index.generate_batch(batch_size)):
        assert len(batch_triple) == 3
        assert all(len(batch) <= batch_size for batch in batch_triple)
        # assert all(batch.shape[1] == 100 for batch in batch_triple)
        # assert all(batch.dtype == np.float for batch in batch_triple)


def test_max_sentence_len(index: Index):
    assert index.max_sentence_length > 0
    print(index.max_sentence_length)


def test_search(index: Index, question):
    results = index.search(question.question, nbest=5)
    assert(len(results) <= 5)
