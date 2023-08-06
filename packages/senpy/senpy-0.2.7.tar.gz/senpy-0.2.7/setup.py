from setuptools import setup
import senpy

setup(
    name='senpy',
    packages=['senpy'],  # this must be the same as the name above
    version=senpy.VERSION,
    description='''
    A sentiment analysis server implementation. Designed to be \
extendable, so new algorithms and sources can be used.
    ''',
    author='J. Fernando Sanchez',
    author_email='balkian@gmail.com',
    url='https://github.com/balkian/senpy',  # use the URL to the github repo
    download_url='https://github.com/balkian/senpy/archive/{}.tar.gz'.format(senpy.VERSION),
    keywords=['eurosentiment', 'sentiment', 'emotions', 'nif'],  # arbitrary keywords
    classifiers=[],
)
