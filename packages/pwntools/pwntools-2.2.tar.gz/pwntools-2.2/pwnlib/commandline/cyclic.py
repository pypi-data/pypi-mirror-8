#!/usr/bin/env python2
import argparse, string, sys
from pwnlib.util import cyclic, packing
from pwnlib import log

parser = argparse.ArgumentParser(
    description = "Cyclic pattern creator/finder"
)

parser.add_argument(
    '-a', '--alphabet',
    metavar = 'alphabet',
    default = string.ascii_lowercase,
    help = 'The alphabet to use in the cyclic pattern (defaults to all lower case letters)',
)

parser.add_argument(
    '-n', '--length',
    metavar = 'length',
    default = 4,
    type = int,
    help = 'Size of the unique subsequences (defaults to 4).'
)

group = parser.add_mutually_exclusive_group(required = True)
group.add_argument(
    '-l', '-o', '--offset', '--lookup',
    dest = 'lookup',
    metavar = '<lookup value>',
    help = 'Do a lookup instead printing the alphabet',
)

group.add_argument(
    'count',
    type = int,
    nargs = '?',
    help = 'Number of characters to print'
)

def main():
    args = parser.parse_args()
    alphabet = args.alphabet
    subsize  = args.length

    if args.lookup:
        pat = args.lookup

        if pat.startswith('0x'):
            pat = packing.pack(int(pat[2:], 16), subsize*8, 'little', 'unsigned')
        elif pat.isdigit():
            pat = packing.pack(int(pat, 10), subsize*8, 'little', 'unsigned')

        if len(pat) != 4:
            log.fatal('Subpattern must be 4 bytes', 1)

        if not all(c in alphabet for c in pat):
            log.fatal('Pattern contains characters not present in the alphabet', 1)

        offset = cyclic.cyclic_find(pat, alphabet, subsize)

        if offset == -1:
            log.fatal('Given pattern does not exist in cyclic pattern', 1)
        else:
            print offset
    else:
        want   = args.count
        result = cyclic.cyclic(want, alphabet, subsize)
        got    = len(result)
        if got < want:
            log.failure("Alphabet too small (max length = %i)" % got)

        sys.stdout.write(result)

        if sys.stdout.isatty():
            sys.stdout.write('\n')

if __name__ == '__main__': main()