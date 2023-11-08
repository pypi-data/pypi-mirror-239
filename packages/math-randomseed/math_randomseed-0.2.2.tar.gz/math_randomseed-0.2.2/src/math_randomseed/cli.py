import argparse
from math_randomseed.math_randomseed import tell_math_joke, get_math_fact

def main1_joke():
    parser = argparse.ArgumentParser(description='Tell a math joke')
    args = parser.parse_args()
    joke = tell_math_joke()
    print(joke + '\n')
if __name__ == '__main__':
    main1()

def main2_fact():
    parser = argparse.ArgumentParser(description='Get a math fact')
    args = parser.parse_args()
    fact = get_math_fact()
    print(fact + '\n')
if __name__ == '__main__':
    main2()