[![Python CI](https://github.com/software-students-fall2023/3-python-package-exercise-random-seed-2/actions/workflows/python-package.yml/badge.svg?branch=lara)](https://github.com/software-students-fall2023/3-python-package-exercise-random-seed-2/actions/workflows/python-package.yml)

# Python Package Exercise

A little exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

## Group Members 
[Lara Kim](https://github.com/larahynkim) <br>
[Andrew Huang](https://github.com/andrewhuanggg) <br>
[Ahmed Omar](https://github.com/ahmed-o-324) <br>
[Henry Wang](https://github.com/fishlesswater) <br>

## Python Package Link
https://pypi.org/project/math-randomseed/0.1.2/ 

## Setting up Virtual Env, Installing Dependencies, and Building and Testing 

1. Install `pipenv`
```
pip install pipenv 
```

2. Install all dependencies from `Pipfile.lock`
```
pipenv --python $(which python3) install
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

6. Run example program
```
python3 example.py
```
