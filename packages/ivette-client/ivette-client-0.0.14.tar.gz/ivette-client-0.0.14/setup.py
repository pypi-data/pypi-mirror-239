from setuptools import setup

setup(
    name='ivette-client',
    version='0.0.14',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['runJob', 'package.IO_module', 'package.prisma_module', 'package.supabase_module'],  # Include 'runJob.py' as a module
    entry_points={
        'console_scripts': [
            'ivette=runJob:main',
        ],
    },
)
