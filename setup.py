#from distutils.core import setup
from setuptools import setup

dependecy_links = ["git+https://github.com/pexpect/pexpect.git#egg=pexpect-0.1"]
install_requires = ['requests']

setup(
    name='rash',
    version='0.91',
    packages=['rash',],
    install_requires=install_requires,
    entry_points = { 'console_scripts': [
        'rash = rash.rash:cli', ],
     },
)
