import pytest 
from math_randomseed.math_randomseed import add, subtract, multiply, divide, get_math_fact, tell_math_joke

##test cases for add function
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_positive_numbers():
    assert add(-1, 1) == 0

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(5, 0) == 5

##test cases for subtract function

def test_subtract_positive_numbers():
    assert subtract(2, 3) == -1

def test_subtract_negative_positive_numbers():
    assert subtract(-1, 1) == -2

def test_subtract_negative_numbers():
    assert subtract(-1, -1) == 0

def test_subtract_zero():
    assert subtract(5, 0) == 5
    
##test cases for multiply function

def test_multiply_positive_numbers():
    assert multiply(2, 3) == 6

def test_multiply_negative_positive_numbers():
    assert multiply(-1, 1) == -1

def test_multiply_negative_numbers():
    assert multiply(-1, -1) == 1

def test_multiply_by_zero():
    assert multiply(5, 0) == 0

##test cases for divide function

def test_divide_positive_numbers():
    assert divide(6, 3) == 2

def test_divide_negative_positive_numbers():
    assert divide(-1, 1) == -1

def test_divide_negative_numbers():
    assert divide(-1, -1) == 1

def test_divide_nonzero():
    assert divide(5, 2) == 2.5

def test_divide_by_one():
    assert divide(5, 1) == 5

def test_divide_by_zero_raises_exception():
    with pytest.raises(ValueError):
        divide(5, 0)

##test cases for math fact function

def test_get_math_fact():
    fact = get_math_fact()
    assert isinstance(fact, str) and len(fact) > 0

def test_math_fact_brevity():
    fact = get_math_fact()
    assert len(fact) <= 280, "The joke should be concise and no longer than 280 characters"

def test_get_math_fact_not_empty():
    fact = get_math_fact()
    assert fact.strip() != ""

##test cases for math joke function

def test_tell_math_joke():
    joke = tell_math_joke()
    assert isinstance(joke, str) and len(joke) > 0
    
def test_tell_math_joke_brevity():
    joke = tell_math_joke()
    assert len(joke) <= 280, "The joke should be concise and no longer than 280 characters"

def test_get_math_joke_not_empty():
    joke = tell_math_joke()
    assert joke.strip() != ""