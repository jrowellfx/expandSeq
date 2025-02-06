# About expandseq and condenseseq

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

The above three cases may be combined to describe
less regular lists of Frame-Ranges by concatenating one
Frame-Range after another separated by spaces or commas.

## Installing the commands

```
python3 -m pip install expandSeq --upgrade
```

## Testing the installation

You should be able to run the following commands and get this output.

```
1$ expandseq 1-10
1 2 3 4 5 6 7 8 9 10
2$ condenseseq 1 2 3 4 5 7 9 11 13 15
1-4 5-15x2
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
  --no-error             skip invalid FRAME-RANGEs, but print warning
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
  --only-ones            only condense sucessive frames, that is, do not list
                        sequences on 2's, 3's, ... N's
  --pad PAD             set the padding of the frame numbers to be <PAD>
                        digits. [default: 1]
  --error               exit with error if FRAME-RANGE is invalid. (default)
  --no-error             skip invalid FRAME-RANGEs, but print warning
  --silent, --quiet     suppress all errors and warnings

```

# Important: latest MAJOR point release of `expandseq`.

`expandseq` and `condenseseq` as well as all
the utilities provided by jrowellfx github repos
use "[`Semantic Versioning 2.0.0`](https://semver.org/)" in numbering releases.
The latest release of `expandseq` upped the `MAJOR` release number
from `v3.x.x` to `v4.x.x`.

While the functionality and output of neither `expandseq` nor
`condenseseq` has changed, all the so called
"long options" have been renamed to adhere to `POSIX` standard naming
conventions.

That is, prior to `v4.0.0` of `expandseq` all the long-option names used a "camel case"
naming convention but as of `v4.0.0` all long-option names have been
changed to so-called "kebab case".

For example:

```
--onlyOnes

```

has been changed to

```
--only-ones
```

In the event that you have written any scripts that make use of `expandseq`,
`condenseseq` or
any other of `jrowellfx`'s utils provided [here](https://github.com/jrowellfx) 
you will need to edit your scripts to be able to update to the lastest versions
of the utilities.

In this case, in order to assist in switching to the
current `MAJOR` point release some `sed` scripts have been provided that should make
the transition quite painless. Especially if you make use
of [`runsed`](https://github.com/jrowellfx/runsed) which if you haven't used it before,
now is the time, it's extremely helpful.

There are two files provided at the root-level of the repo, namely:
`sed.script.jrowellfx.doubleDashToKebab` and `sed.script.expandseq.v3tov4`.

The first one can be used to fix the long-option names for ALL the 
`MAJOR` point release updates to the long-options in any of `jrowellfx`'s utilities.
The second one contains only changes needed for the updates to `expandseq`
or `condenseseq`.

## Example `sed.script` usage.

Download one or both of the sed scripts named above. Make sure you have runsed installed
on your system. (Example applied to usage of `lsseq` but it's
the same idea for `expandseq`.)

```
$ cd ~/bin
$ ls
myScriptThatUsesLsseq
$ cat myScriptThatUsesLsseq
#!/bin/bash

lsseq --globalSortByTime --recursive --prependPathAbs /Volumes/myProjectFiles

$ mv ~/Downloads/sed.script.jrowellfx.doubleDashToKebab sed.script
$ runsed myScriptThatUsesLsseq
$ ./.runsed.diff.runsed
+ /usr/bin/diff ./.myScriptThatUsesLsseq.runsed myScriptThatUsesLsseq
3c3
< lsseq --globalSortByTime --recursive --prependPathAbs /Volumes/myProjectFiles
---
> lsseq --global-sort-by-time --recursive --prepend-path-abs /Volumes/myProjectFiles
$ cat myScriptThatUsesLsseq
#!/bin/bash

lsseq --global-sort-by-time --recursive --prepend-path-abs /Volumes/myProjectFiles
```

Note that if you are unhappy with the changes you can undo them easily with

```
$ ./.runsed.undo.runsed
$ cat myScriptThatUsesLsseq
#!/bin/bash

lsseq --globalSortByTime --recursive --prependPathAbs /Volumes/myProjectFiles


```

## Contact

Please contact `j a m e s <at> a l p h a - e l e v e n . c o m` with any bug
reports, suggestions or praise as the case may be.

