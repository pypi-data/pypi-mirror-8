"""
Entry point for console script jp2dump.
"""
import argparse
import sys
import warnings
from . import Jp2k, set_printoptions

def main():
    """
    Entry point for console script jp2dump.
    """

    description='Print JPEG2000 metadata.'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-x', '--noxml',
            help='Suppress XML.',
            action='store_true')
    parser.add_argument('-s', '--short',
            help='Only print box id, offset, and length.',
            action='store_true')

    chelp = 'Level of codestream information.  0 suppressed all details, '
    chelp += '1 prints headers, 2 prints the full codestream'
    parser.add_argument('-c', '--codestream',
            help=chelp,
            nargs=1,
            type=int,
            default=[0])

    parser.add_argument('filename')

    args = parser.parse_args()
    if args.noxml:
        set_printoptions(xml=False)
    if args.short:
        set_printoptions(short=True)
    
    codestream_level = args.codestream[0]
    if codestream_level not in [0, 1, 2]:
        raise ValueError("Invalid level of codestream information specified.")

    if codestream_level == 0:
        set_printoptions(codestream=False)
        print_full_codestream = False
    elif codestream_level == 1:
        print_full_codestream = False
    else:
        print_full_codestream = True
    
    filename = args.filename
    
    with warnings.catch_warnings(record=True) as wctx:

        # JP2 metadata can be extensive, so don't print any warnings until we
        # are done with the metadata.
        j = Jp2k(filename)
        if print_full_codestream:
            print(j.get_codestream(header_only=False))
        else:
            print(j)

        # Re-emit any warnings that may have been suppressed.
        if len(wctx) > 0:
            print("\n")
        for warning in wctx:
            print("{0}:{1}: {2}: {3}".format(warning.filename,
                                             warning.lineno,
                                             warning.category.__name__,
                                             warning.message))
