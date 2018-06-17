from product_team import Index,Question
import pytest

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
import json
@pytest.fixture
def question():
    return Question(**test_question)

@pytest.fixture
def index(question):
    ret = Index()
    ret.index(question)
    return ret


def test_index(index : Index):
    assert len(index.documents) > 0
