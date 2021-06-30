from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='expandSeq',
    version='0.0.1',
    description='Command line utils to expose functionality of seqLister python library.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/jrowellfx/expandSeq',
    author='James Philip Rowell',
    author_email='james@alpha-eleven.com',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Linux',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Development Status :: 5 - Production/Stable',
    ],

    keywords='vfx, shot-td, image-sequence',
    package_dir={'', 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['seqLister'],

    entry_points={  # Optional
        'console_scripts': [
            'expandseq=expandseq.__main__:main',
            'condenseseq=expandseq.__main__:main',
        ],
    },
)
