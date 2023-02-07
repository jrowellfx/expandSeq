.ll 70
.na
.hy 0
.pl 1
Expands a list of integers and integer sequences
of the form 'A-B' or 'A-BxN' into a list of integers.

A-BxN means list every Nth integer starting at A ending at the highest integer
less than or equal to B. Numbers will only be listed once each.
That is; '2-4 1-6' yeilds the list '2 3 4 1 5 6'. 

.in +4 
Helpful hint: To pass negative numbers to the command use
a double-minus '--' to signify the end of OPTIONS.
.br
For example:

.in +4 
"-- -12" or "-- -99-86",
.in -4 

allows you to pass a minus-twelve, or minus-ninety-nine through
eighty-six to the command without it being interpreted as an OPTION.
.in -4 

(Also see condenseseq).

-------------

Condenses a list of integers and/or integer sequences
of the form
.br
\'A-B' or 'A-BxN' into the most minimal sequence format
possible to represent the full list of numbers.

INCLUDE HELPFUL HINT HERE AS WELL.

(Also see expandseq).


For example:


