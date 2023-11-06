# Python Package Exercise

A little exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

### Setting up Virtual Env, Installing Dependencies, and Building and Testing 

1. Install `pipenv`
```
pip install pipenv 
```

2. Install all dependencies from `Pipfile.lock`
```
pipenv install
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
pytest
```

6. Run example program
```
python3 example.py
```