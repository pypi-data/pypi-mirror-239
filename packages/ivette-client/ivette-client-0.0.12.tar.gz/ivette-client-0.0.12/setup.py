from setuptools import setup

setup(
    name='ivette-client',
    version='0.0.12',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['runJob', 'package'],  # Include 'runJob.py' as a module
    entry_points={
        'console_scripts': [
            'ivette=runJob:main',
        ],
    },
)
