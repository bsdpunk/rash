#from distutils.core import setup
from setuptools import setup

setup(
    name='rash',
    version='0.2',
    packages=['rash',],
    entry_points = {
        'console_scripts': [
            'rash = rash.rash:cli',
        ]
    }
)
