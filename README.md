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
