#!/usr/bin/env python3

# 3-Clause BSD License
# 
# Copyright (c) 2008-2023, James Philip Rowell,
# Alpha Eleven Incorporated
# www.alpha-eleven.com
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
# 
#  3. Neither the name of the copyright holder, "Alpha Eleven, Inc.",
#     nor the names of its contributors may be used to endorse or
#     promote products derived from this software without specific prior
#     written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# expandseq/condenseseq - two command line utilities that expose the basic
# functionality of the python-module "seqLister.py" functions "expandSeq()"
# and "condenseSeq()".  These functions translate back and forth between a
# condensed form for listing sequences of integers and plain lists of integers.
# Lists of integers in this condensed format are commonly used by various
# computer programs dealing with sequences of images such as render farm
# management tools (like smedge), image sequence viewers (like rv) or "ls"
# commands (like lsseq) to list frames from CG-animation or video footage
# which has been saved as a sequence of individually numbered frames.
#
# The "expandseq" and "condenseseq" commands enhance the simple behavior of
# the "expandSeq()" and "condenseSeq()" python functions by adding the ability
# to print out the lists in various forms.  eg.; comma, space or newline
# separators as well as sorting the lists, reversing order, and mixing and
# matching expanded and condensed formats as arguments on the command line.

import argparse
import os
import sys
import subprocess
import textwrap
from operator import itemgetter
import seqLister

# MAJOR version for incompatible API changes
# MINOR version for added functionality in a backwards compatible manner
# PATCH version for backwards compatible bug fixes
#
VERSION     = "3.0.0"

PROG_NAME = "condenseseq"

def main():

    # Redefine the exception handling routine so that it does NOT
    # do a trace dump if the user types ^C while expandseq or
    # condenseseq are running.
    #
    old_excepthook = sys.excepthook
    def new_hook(exceptionType, value, traceback):
        if exceptionType != KeyboardInterrupt and exceptionType != IOError:
            old_excepthook(exceptionType, value, traceback)
        else:
            pass
    sys.excepthook = new_hook

    p = argparse.ArgumentParser(

    formatter_class=argparse.RawDescriptionHelpFormatter,
        prog=PROG_NAME,
        description=textwrap.dedent('''\
            Given a list of 'Frame-Ranges' condense the fully expanded list into
            the most succinct list of 'Frame-Ranges' possible.

            Definition: 'Frame-Range'
                Given that 'A', 'B' and 'N' are integers, then a 'Frame-Range' is one,
                or any combination, of the following:

                   'A'     the integer A.

                   'A-B'   all the integers from A to B inclusive.

                   'A-BxN' every Nth integer starting at A and increasing to be no
                           larger than B when A < B, or decreasing to be no less
                           than B when A > B.

            'Frame-Ranges' may be combined to describe less regular sequences by
            concatenating one after another separated by spaces or commas.

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

            (Also see expandseq).
            '''),
        usage="%(prog)s [OPTION]... [FRAME-RANGE]...")

    p.add_argument("--version", action="version", version=VERSION)
    p.add_argument("--delimiter", "-d", action="store", type=str,
        choices=("comma", "space", "newline"),
        dest="seqDelimiter",
        metavar="DELIMITER",
        default="space",
        help="List successive numbers delimited by a 'comma', 'space' (default) or a 'newline'.")
    p.add_argument("--onlyOnes", action="store_true",
        dest="onlyOnes", default=False,
        help="only condense sucessive frames, that is, do not list sequences on 2's, 3's, ... N's")
    p.add_argument("--pad", action="store", type=int,
       dest="pad", default=1,
       metavar="PAD",
       help="set the padding of the frame numbers to be <PAD> digits. [default: 1]")
    p.add_argument("--reverse", "-r", action="store_true",
        dest="reverseList", default=False,
        help="reverse the order of the list")
    p.add_argument("numSequences", metavar="FRAME-RANGE", nargs="*",
        help="See the definition of 'FRAME-RANGE' above.")

    # Copy the command line args (except prog name) and convert
    # commas into spaces thus making more args.
    #
    args = p.parse_args()

    separateArgs = []
    for a in args.numSequences :
        for b in a.split(',') :
            separateArgs.append(b)
    remainingArgs = []
    expandedArgs = seqLister.expandSeq(separateArgs, remainingArgs)

    # WARNING? if remainingArgs is nonzero length? based on new flag?

    # Sort the list before passing to condenseq(), as it won't make a difference
    # to the output, unless the user wants the list reversed, then this will 
    # create a properly reversed set of FRAME-RANGES.
    #
    expandedArgs.sort()
    if args.reverseList :
        expandedArgs.reverse()

    tmp = []
    if args.onlyOnes :
        result = seqLister.condenseSeqOnes(expandedArgs, args.pad, tmp)
        # tmp should be zero length since expandSeq above should have caught issues.
    else :
        result = seqLister.condenseSeq(expandedArgs, args.pad, tmp)

    isFirst = True
    for s in result :
        if args.seqDelimiter == 'space' :
            if not isFirst :
                sys.stdout.write(' ')
            sys.stdout.write(str(s))
            isFirst = False
        elif args.seqDelimiter == 'comma' :
            if not isFirst :
                sys.stdout.write(',')
            sys.stdout.write(str(s))
            isFirst = False
        else : # newline
            print(s)
    if (args.seqDelimiter == 'comma' or args.seqDelimiter == 'space') and not isFirst :
        print()

if __name__ == '__main__':
    main()
