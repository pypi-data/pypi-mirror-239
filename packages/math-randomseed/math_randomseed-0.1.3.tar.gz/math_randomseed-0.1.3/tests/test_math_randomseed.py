import pytest 
from math_randomseed.math_randomseed import add, subtract, multiply, divide, get_math_fact


def test_add():
    assert add(2,3) == 5
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2
    assert add(5,0) == 5

def test_subtract():
    assert subtract(2, 3) == -1
    assert subtract(-1, 1) == -2
    assert subtract(-1, -1) == 0
    assert subtract(5, 0) == 5
    

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1
    assert multiply(5, 0) == 0


def test_divide():
    assert divide(6, 3) == 2
    assert divide(-1, 1) == -1
    assert divide(-1, -1) == 1
    assert divide(5, 2) == 2.5
    assert divide(5, 1) == 5
    with pytest.raises(ValueError):
        divide(5, 0)

def test_get_math_fact():
    fact = get_math_fact()
    assert isinstance(fact, str) and len(fact) > 0