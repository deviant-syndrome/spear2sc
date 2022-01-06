# -*- coding: utf-8 -*-


"""spear2sc.spear2sc: provides entry point main()."""

__version__ = "0.1.0"

import sys
import argparse
from .lib import convert, read_spear_file
from .analysis import print_analysis


def main():
    parser = argparse.ArgumentParser(description='SPEAR2SC %s. SuperCollider-friendly Spear file reader' % __version__)
    parser.add_argument('input',
                        help='Input file name in Spear format')
    parser.add_argument('output', nargs='?', default=None,
                        help='Output file, if not specified, only source file analysis will be performed')
    parser.add_argument('--max-partials', '-m', nargs='?', const=42, default=42, type=int,
                        help='Maximum number of partials to write')
    parser.add_argument('--part-dur-thresh', '-d', nargs='?', type=float,
                        help='Partial duration threshold, secs')
    parser.add_argument('--part-lev-thresh', '-a', nargs='?', const=0.0, default=0.0, type=float,
                        help='Partial median level threshold, [0..1]')
    parser.add_argument('--plot', '-p', action='store_true',
                        help='Plot partial level envelopes and duration distributions to console')

    args = parser.parse_args()
    if args.output is None:
        print_analysis(read_spear_file(args.input), (args.part_dur_thresh, args.part_lev_thresh, args.plot))
        quit()

    print("List of argument strings: %s" % sys.argv[1:])
    num_read, num_written = convert(sys.argv[1], sys.argv[2], (args.part_dur_thresh, args.part_lev_thresh, args.max_partials))
    print("Conversion completed. Written {}/{} ({:6.2f}%) partials".format(num_written, num_read, num_written / (num_read + 0.0001) * 100))
