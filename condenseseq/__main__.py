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

# expandseq/condenseseq - two command line utilities that expose and
# expand upon the basic functionality of the python-module "seqLister"
# functions "expandSeq()" and "condenseSeq()".

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
            Given a list of FRAME-RANGEs condense the fully expanded list into
            the most succinct list of FRAME-RANGEs possible.

            Definition: FRAME-RANGE
                Given that 'A', 'B' and 'N' are integers, then a FRAME-RANGE is one,
                or any combination, of the following:

                   'A'     the integer A.

                   'A-B'   all the integers from A to B inclusive.

                   'A-BxN' every Nth integer starting at A and increasing to be no
                           larger than B when A < B, or decreasing to be no less
                           than B when A > B.

            FRAME-RANGEs may be combined to describe less regular sequences by
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

    p.add_argument("--error", action="store_true",
        dest="exitOnError", default=True,
        help="exit with error if FRAME-RANGE is invalid. (default)" )
    p.add_argument("--noError", action="store_false",
        dest="exitOnError",
        help="skip invalid FRAME-RANGEs, but print warning" )

    p.add_argument("--silent", "--quiet", action="store_true",
        dest="silent", default=False,
        help="suppress all errors and warnings")

    p.add_argument("numSequences", metavar="FRAME-RANGE", nargs="*",
        help="See the definition of 'FRAME-RANGE' above.")

    args = p.parse_args()

    # Copy the command line args converting commas into spaces and then 
    # splitting along ALL whitespace possibly generating more args.
    #
    separateArgs = []
    for a in args.numSequences :
        for b in a.split(',') :
            for c in b.split() :
                separateArgs.append(c)
    remainingArgs = []

    # Now fully expand all the FRAME-RANGES supplied to get a FULL set of frame
    # numbers before condensing the full list.
    #
    expandedArgs = seqLister.expandSeq(separateArgs, remainingArgs)

    # Any non-FRAME-RANGES, should have been caught at this point, so we can
    # process the possible errors and warnings now. Same code as expandSeq command.
    #
    # Check for any invalid FRAME-RANGEs, and respond according to
    # flags set with OPTIONS. Only show up to 3 bad FRAME-RANGES,
    # chop any after that and append an 'etc.' note to the warning
    # or error message.
    #
    badArgsLength = len(remainingArgs)
    if badArgsLength > 0 :

        badArgsEtcLength = badArgsLength
        if badArgsLength > 3 :
            badArgsEtcLength = 3

        plural = ''
        count = ''
        if badArgsLength > 1 :
            plural = 's'
            count = str(badArgsLength) + ' '

        badFramesMessage = count \
            + 'invalid FRAME-RANGE' \
            + plural + ': ' \
            + ', '.join(remainingArgs[:badArgsEtcLength])

        if badArgsLength > 3 :
            badFramesMessage += ', ... etc.'

        if args.exitOnError :
            if not args.silent :
                print(PROG_NAME,
                    ": error: ", badFramesMessage,
                    file=sys.stderr, sep='')
            sys.exit(1)
        else :
            if not args.silent :
                print(PROG_NAME,
                    ": warning: ", badFramesMessage,
                    file=sys.stderr, sep='')

    tmpList = []
    if args.onlyOnes :
        result = seqLister.condenseSeqOnes(expandedArgs, args.pad, tmpList)

        # tmpList should be zero length since expandSeq() call above should
        # have caught all the issues with badly formed FRAME-RANGEs.
        #
        if len(tmpList) > 0 and not args.silent :
            print(PROG_NAME,
                ": ASSERT FAILURE: call to seqLister.condenseSeqOnes() returned non-zero length nonSeqList.",
                file=sys.stderr, sep='')
    else :
        result = seqLister.condenseSeq(expandedArgs, args.pad, tmpList)

        # tmpList should be zero length since expandSeq() call above should
        # have caught all the issues with badly formed FRAME-RANGEs.
        #
        if len(tmpList) > 0 and not args.silent :
            print(PROG_NAME,
                ": ASSERT FAILURE: call to seqLister.condenseSeq() returned non-zero length nonSeqList.",
                file=sys.stderr, sep='')

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
