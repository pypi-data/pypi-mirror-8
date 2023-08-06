import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))

setup(
    name='pymza',
    version='0.2',
    author="Sergey Kirillov",
    author_email="sergey.kirillov@gmail.com",
    description="Streaming data processing framework inspired by Apache Samza.",
    packages=['pymza'],
    install_requires=[
        'Click',
        'gevent',
        #'kafka-python>=0.9.3',  # not released yet, install manually
        'leveldb',
    ],
    entry_points='''
        [console_scripts]
        pymza=pymza.cli:main
    ''',
    long_description=open(os.path.join(here, 'README.rst'), 'rb').read().decode('utf-8')
)