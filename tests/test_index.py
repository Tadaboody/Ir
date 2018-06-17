import json

import pytest

from product_team import Question, load_index, Index

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

@pytest.fixture
def question():
    return Question(**test_question)

@pytest.fixture(scope="session")
def index():
    return load_index() 

# @pytest.fixture
# def index(question):
#     ret = Index('/')
#     ret.add_doc(question)
#     return ret


def test_empty_index(index : Index):
    assert len(index.documents) > 0

def test_search(index: Index, question : Question):
    results = index.search(question.question,nbest=5)
    assert(len(results) <= 5)
