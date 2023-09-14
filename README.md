# About expandseq and consdenseseq

`expandseq` and `condenseseq` are two unix/linux command-line utilitiies 
for expanding and condensing
integer-sequences using a simple syntax widely used within
the VFX-industry for specifying frame-ranges.

## Definition: 'Frame-Range'.

Given that 'A', 'B' and 'N' are integers, the syntax
for specifying an integer sequence used to describe
frame-ranges is one of the following three cases:

1. 'A' : just the integer A.

2. 'A-B' : all the integers from A to B inclusive.

3. 'A-BxN' : every Nth integer starting at A and increasing
to be no larger than B when A < B, or descending
to be no less than B when A > B.

The above three cases may often be combined to describe
less regular lists of Frame-Ranges by concatenating one
Frame-Range after another separated by spaces or commas.

## Installing the commands

python3 -m pip install expandSeq

## Testing the installation

You should be able to run the following commands and get this output.

```
1$ expandseq 1-10
1,2,3,4,5,6,7,8,9,10
2$ condenseseq 1 2 3 4 5 7 9 11 13 15
1-4,5-15x2
```

## expandseq

```
expandseq [OPTION]... [FRAME-RANGE]...

Expands a list of FRAME-RANGEs into a list of integers.

Example:
    $ expandseq 2-4 1-6 10
    2 3 4 1 5 6 10

Note in the above example that numbers are only listed once each.
That is, once '2-4' is listed, then '1-6' only need list 1, 5 and 6.

More examples:
    $ expandseq 1-10x2, 20-60x10
    1 3 5 7 9 20 30 40 50 60
    $ expandseq --pad 3 109-91x4
    109 105 101 097 093
    $ expandseq --pad 4 -- -99-86x23
    -099 -076 -053 -030 -007 0016 0039 0062 0085

Protip: To pass a negative-number to expandseq WITHOUT it being intepreted
as a command-line OPTION insert a double-minus ('--') before the
negative-number, which is a standard technique to deliniate the end
of command-line options.

positional arguments:
  FRAME-RANGE           See the definition of 'FRAME-RANGE' above.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --delimiter DELIMITER, -d DELIMITER
                        List successive numbers delimited by a 'comma',
                        'space' (default) or a 'newline'.
  --pad PAD             set the padding of the frame numbers to be <PAD>
                        digits. [default: 1]
  --reverse, -r         reverse the order of the list
  --sort, -s            sort the resulting list
  --error               exit with error if FRAME-RANGE is invalid. (default)
  --noError             skip invalid FRAME-RANGEs, but print warning
  --silent, --quiet     suppress all errors and warnings
```

## condenseseq

```
condenseseq [OPTION]... [FRAME-RANGE]...

Given a list of FRAME-RANGEs condense the fully expanded list into
the most succinct list of FRAME-RANGEs possible.

Examples:
    $ condenseseq 1-100x2 2-100x2
    1-100
    $ condenseseq 0-100x2 51
    0-50x2 51 52-100x2
    $ condenseseq --pad 3 49 0-100x2 51 53
    000-048x2 049-053 054-100x2

Protip: To pass a negative-number to expandseq WITHOUT it being intepreted
as a command-line OPTION insert a double-minus ('--') before the
negative-number, which is a standard technique to deliniate the end
of command-line options.

positional arguments:
  FRAME-RANGE           See the definition of 'FRAME-RANGE' above.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --delimiter DELIMITER, -d DELIMITER
                        List successive numbers delimited by a 'comma',
                        'space' (default) or a 'newline'.
  --onlyOnes            only condense sucessive frames, that is, do not list
                        sequences on 2's, 3's, ... N's
  --pad PAD             set the padding of the frame numbers to be <PAD>
                        digits. [default: 1]
  --error               exit with error if FRAME-RANGE is invalid. (default)
  --noError             skip invalid FRAME-RANGEs, but print warning
  --silent, --quiet     suppress all errors and warnings

```
