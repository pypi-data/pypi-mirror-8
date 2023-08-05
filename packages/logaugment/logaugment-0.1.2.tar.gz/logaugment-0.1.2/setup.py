from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as file_readme:
    long_description = file_readme.read()


setup(
    name='logaugment',
    version='0.1.2',
    description='Python logging library for augmenting log records with additional information',
    long_description=long_description,
    url='https://github.com/svisser/logaugment',
    download_url='https://pypi.python.org/pypi/logaugment',
    author='Simeon Visser',
    author_email='simeonvisser@gmail.com',
    license='MIT',
    packages=['logaugment'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Logging',
    ],
    keywords='python custom logging keys keywords values'
)
