# About expandseq and consdenseseq

`expandseq` and `condenseseq`are two unix/linux command-line utilitiies that
expose the functionality of the python library package `seqLister` to shell users.

## Installing the commands

python3 -m pip install expandSeq

## Testing the installation

You should simply be able to run the commands now.

```
1$ expandseq 1-10
1,2,3,4,5,6,7,8,9,10
2$ condenseseq 1 2 3 4 5 7 9 11 13 15
1-4,5-15x2
```
