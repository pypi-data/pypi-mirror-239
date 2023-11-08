from setuptools import setup, find_packages

setup(
    name='math_randomseed',
    version='0.2.3',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts':[
            'tell_math_joke = math_randomseed.cli:main1_joke',
            'get_math_fact = math_randomseed.cli:main2_fact'
        ],
    }
)
