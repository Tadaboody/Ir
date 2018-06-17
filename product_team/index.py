""" Module for basic index classes"""
from typing import Iterator
from collections import namedtuple
import json
Question = namedtuple(
    'Question', ['id','question', 'nbestanswers', 'answer', 'main_category'])


class Index:
    """ Base class for an index of questions"""
    def __init__(self):
        self.documents = list()  # List[Question]
        

    @classmethod
    def from_file(cls, path: str): # -> Index
        """ Factory method for creating an index from a json"""
        self = cls()
        with open(path) as fp:
            question_list = json.load(fp)
        for question in question_list:
            self.index(Question(**question))
        return self

    def index(self, question: Question):
        """ Indexes a single question """
        self.documents.append(question)
    
    def all_answers(self) -> Iterator[str]:
        for question in self.documents:
            for answer in question.nbestanswers:
                yield answer