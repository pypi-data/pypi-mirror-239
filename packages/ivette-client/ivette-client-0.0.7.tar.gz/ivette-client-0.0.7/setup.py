from setuptools import setup

setup(
    name='ivette-client',
    version='0.0.7',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    packages=['package'],
    entry_points={
        'console_scripts': [
            'ivette=runJob',
        ],
    },
)
