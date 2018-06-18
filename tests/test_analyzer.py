import string

import pytest

from product_team import EnglishAnalyzer
from product_team.analyzer import stopwords


@pytest.fixture
def analyzer():
    return EnglishAnalyzer()


def test_posessive(analyzer: EnglishAnalyzer):
    strings_with_posessive = ["mike's", "U.S.A's Constitution'S"]
    filtered_strings = [analyzer.EnglishPosessiveFilter(
        token) for token in strings_with_posessive]
    assert all("'s" not in token for token in filtered_strings)
    assert all("'S" not in token for token in filtered_strings)


def test_stop_filter(analyzer: EnglishAnalyzer):
    tokens_with_stops = ['the', 'and', 'usa', 'iran', 'or']
    assert(all(word not in analyzer.StopFilter(tokens_with_stops)
               for word in stopwords))


def assert_punct_less(token: str):
    assert(all(punct not in token for punct in string.punctuation))


def test_punctuation_filter(analyzer: EnglishAnalyzer):
    tokens_with_stops = ['where?', 'you!', 'wh?o?', 'gpas.', 'that!)']
    tokens_without_stops = analyzer.PunctuationFilter(tokens_with_stops)
    for token in tokens_without_stops:
        assert_punct_less(token)


def test_no_tokens(analyzer: EnglishAnalyzer):
    sentance = "is'!"
    token = analyzer.tokenize(sentance)
    assert token is None


def test_all_filters(analyzer: EnglishAnalyzer):
    sentance = "iran!? no way. ' the place is not iran's but israel's!"
    tokens = analyzer.tokenize(sentance)
    for token in tokens:
        assert_punct_less(token)
        assert token not in stopwords
        assert token.islower()
        assert token != ''


def test_repeat(analyzer: EnglishAnalyzer):
    sentance = "what is the usa?"
    assert analyzer.tokenize(sentance) == analyzer.tokenize(
        analyzer.tokenize(sentance))
