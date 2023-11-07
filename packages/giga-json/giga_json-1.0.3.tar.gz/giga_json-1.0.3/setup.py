import os
from setuptools import setup, find_packages

setup(
    name='giga_json',
    version='1.0.3',
    author='nebko16',
    author_email='nebko16@gmail.com',
    description=("extension of python json module, but dumps pretty prints by default and the serializer can handle almost any python object you give it"),
    license='GPL-3.0',
    keywords='python python3 json giga gigajson giga_json module pprint dumps indent prettyprint pretty print format serializer',
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    url='https://github.com/nebko16/giga_json'
)
