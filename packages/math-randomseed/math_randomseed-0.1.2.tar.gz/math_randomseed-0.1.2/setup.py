from setuptools import setup, find_packages

setup(
    name='math_randomseed',
    version='0.1.2',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.11, <3.13',
    tests_require=[
        'pytest>=6.2', 
    ],
)
