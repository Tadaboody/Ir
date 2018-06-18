import json

import pytest

from product_team import load_index, Index

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
def test_word2vec_vocab(index : Index):
    for sentance in index.Corpus_iterator(index):
        assert index.model[sentance].shape[1] == 100

def test_batches(index : Index):
    batch_size = 30
    for _,batch in zip(range(3),index.generate_batch(batch_size)):
        assert len(batch) <= batch_size
        assert all(len(triple) == 3 for triple in batch)

def test_empty_index(index : Index):
    assert len(index.documents) > 0

def test_search(index: Index, question):
    results = index.search(question.question,nbest=5)
    assert(len(results) <= 5)
