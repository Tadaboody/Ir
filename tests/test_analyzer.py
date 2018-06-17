import pytest
from product_team import EnglishAnalyzer

@pytest.fixture
def analyzer():
    return EnglishAnalyzer()

def test_posessive(analyzer : EnglishAnalyzer):
    strings_with_posessive = ["mike's", "U.S.A's Constitution'S"]
    assert all("'s" not in analyzer.EnglishPosessiveFilter(token) for token in strings_with_posessive)