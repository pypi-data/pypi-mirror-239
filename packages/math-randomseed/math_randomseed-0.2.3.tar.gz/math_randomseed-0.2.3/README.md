[![Python CI](https://github.com/software-students-fall2023/3-python-package-exercise-random-seed-2/actions/workflows/python-package.yml/badge.svg?branch=lara)](https://github.com/software-students-fall2023/3-python-package-exercise-random-seed-2/actions/workflows/python-package.yml)

# Python Package Exercise

The Math RandomSeed Python package is a lightweight library designed to bring a bit of fun to math operations. With simple addition, subtraction, multiplication, division functions, and quirky mathematical facts and jokes, the package is both entertaining and auxiliary. The project follows conventional software engineering practices with testing, proper packaging, and clear instructions for easy distribution.
Documentation for all functions and instructions for installing are detailed below.

## Group Members 
[Lara Kim](https://github.com/larahynkim) <br>
[Andrew Huang](https://github.com/andrewhuanggg) <br>
[Ahmed Omar](https://github.com/ahmed-o-324) <br>
[Henry Wang](https://github.com/fishlesswater) <br>

## Python Package Link
https://pypi.org/project/math-randomseed/0.2.3/

## Package Functions
1. **add(x, y)**:<br>
Adds two numbers together.
2. **subtract(x, y)**:<br>
Subtracts the second number from the first.
3. **multiply(x, y)**:<br>
Multiplies two numbers.
4. **divide(x, y)**:<br>
Divides the first number by the second. Raises a ValueError for division by zero.
5. **get_math_fact()**:<br>
Returns a random fun math fact as a string.
6. **tell_math_joke()**:<br>
Returns a math-themed joke as a string.

See [example.py](./example.py) for, well, an example.


## Setting up Virtual Env, Installing Dependencies, and Building and Testing 

1. Install `pipenv`
```
pip install pipenv 
```

2. Install all dependencies from `Pipfile.lock`
```
pipenv --python $(which python3) install
```
Or if you are using powershell:
```
pipenv --python $(where.exe python3) install
```

3. Activate the virtual environment
```
pipenv shell 
```

4. Install the package
```
pipenv install -e . 
```

5. Run tests
```
pip install -U pytest

pytest
```
If the pytest shows ImportError, try to install python 3.8 and start from beginning

6. Run an example program
```
python3 example.py
```
or
```
python example.py
```
7. Tell a math joke, from the command line
```
tell_math_joke
```
8. Get a math fact, from the command line
```
get_math_fact
```

## Installation and Usage 
To install the most recent version of 'math-randomseed' as a PyPI package, simply run the following command in your terminal: 
```
pip install math-randomseed --upgrade 
```
or 
```
pip3 install math-randomseed --upgrade
```

To use 'math-randomseed' in your project, import the desired functions as follows: 
```
from math_randomseed import add, subtract, multiply, divide, get_math_fact, tell_math_joke
```
## Command Line Capability 
1. Type `tell_math_joke` into the command line to tell a math joke.
2. Type `get_math_fact` into the command line to give a math fact.