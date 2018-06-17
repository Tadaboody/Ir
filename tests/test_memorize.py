import json

from product_team.utils import memorize
import pytest


@pytest.fixture
def function():
    @memorize()
    def foo(a):
        return [str(a)]
    return foo

def test_memorize(function):
    assert function(2) == function(4)
