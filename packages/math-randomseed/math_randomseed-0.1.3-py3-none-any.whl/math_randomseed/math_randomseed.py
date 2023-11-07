import random

def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def get_math_fact():
    """Return a random fun fact about math."""
    fun_facts = [
        "Zero is the only number that can't be represented in Roman numerals.",
        "A circle has 360 degrees because the ancient Sumerians considered 360 to be a perfect number.",
        "The word 'hundred' comes from the old Norse term, 'hundrath', which actually means 120 and not 100.",
        "In a room of 23 people there’s a 50% chance that two people have the same birthday. It's called the Birthday Paradox.",
        "The symbol for division (÷) is called an obelus.",
        "There are 2.4 million different ways to make change for a US dollar.",
        "The Pythagorean theorem was known and used by the Babylonians and Indians centuries before Pythagoras, but he may have been the first to prove it."
    ]
    return random.choice(fun_facts)