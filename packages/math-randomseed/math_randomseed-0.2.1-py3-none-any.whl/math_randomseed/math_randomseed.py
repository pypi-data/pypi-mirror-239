import random

def add(a, b):
    print("")
    """Add two numbers."""
    return a + b
    print("")

def subtract(a, b):
    print("")
    """Subtract b from a."""
    return a - b
    print("")

def multiply(a, b):
    print("")
    """Multiply two numbers."""
    return a * b
    print("")

def divide(a, b):
    print("")
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
    print("")

def get_math_fact():
    print("")
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
    print("")

# tell a math one liner joke
def tell_math_joke():
    print("")
    math_jokes = [
        'To the man who invented zero: Thanks for nothing.',
        'I, for one, like Roman numerals.',
        'Pure mathematicians are like lighthouses in the middle of a swamp — brilliant, but completely useless.',
        "I'm not worried about losing my job to a computer. They've yet to invent a machine that does absolutely nothing.",
        'For every complex mathematical problem, there is a simple and elegant solution that is completely wrong.',
        'y = mx + b',
        'So a Roman walks into a bar, holds up two fingers and says, "I`ll like five beers, please."',
        'I find negative numbers so confusing I will stop at nothing to avoid them!',
        'I poured root beer into a square cup. Now I have beer.'
    ]
    return random.choice(math_jokes)
    print("")