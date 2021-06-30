from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name            = 'expandSeq',
    version         = '0.0.1',
    packages        = ['expandseq'],
    url             = 'https://github.com/jrowellfx/expandSeq',
    author          = 'James Philip Rowell',
    author_email    = 'james@alpha-eleven.com',
    python_requires = '>=3.6, <4',

    entry_points = {
        'console_scripts': [
            'expandseq = expandseq.__main__:main',
            'condenseseq = expandseq.__main__:main'
        ]
    }
)
