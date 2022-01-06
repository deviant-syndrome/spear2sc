# -*- coding: utf-8 -*-

"""spear2sc.lib: Spear2SC API methods
This module contains public methods of the package, that are re-used in package runnable, and also
available via import.
Module itself provides the following methods:

 - read_spear_file(filename): reads data from SPEAR into the list of partials
 - convert(input, output, options): writes list of partials to CSV file, that can be directly digested by SuperCollider
"""

import csv

from publication import publish

from .analysis import get_amp_mean, get_total_duration, get_amp_envelope, get_durations_thresh
from .spear_utils import process_line, get_durations, index_amp, index_freq


def read_spear_file(input_file):
    """Reads SPEAR particle file into a list of partials
    :param input_file: Path to file
    :type input_file: str
    :returns: a list of of list of numbers, representing each partial's level and freq envelope over time
    :rtype: list
    """
    with open(input_file, 'r') as f:
        lines = f.readlines()

    partials = [process_line(line) for line in lines if len(line) >= 57]
    return partials


def convert(input_file, output_file, options):
    """Converts an input SPEAR particle file into a CSV file, that can be directly digested by SuperCollider
    :param input_file: Path to source file
    :type input_file: str
    :param output_file: Path to target file
    :type output_file: str
    :param options: Conversion options (duration threshold, level threshold, max partials)
    :type options: (float, float, int)

    :return:
    """
    dur_thresh, amp_thresh, max_partials = options

    partials = read_spear_file(input_file)

    if dur_thresh is None:
        dur_thresh = get_durations_thresh(partials)

    f = open(output_file, 'w')
    w = csv.writer(f, delimiter=',', lineterminator='\n')

    num_partials_written = 0
    num_partials_read = 0
    for partial in partials:
        num_partials_read = num_partials_read + 1
        if get_total_duration(partial) >= dur_thresh and get_amp_mean(partial) >= amp_thresh and num_partials_written <= max_partials:
            w.writerow(get_durations(partial))
            w.writerow(list(map(lambda p: p[index_freq], partial)))
            w.writerow(list(map(lambda p: p[index_amp], partial)))
            num_partials_written = num_partials_written + 1
    f.close()
    return num_partials_read, num_partials_written


__all__ = [
    'read_spear_file',
    'convert',
    'get_total_duration',
    'get_amp_envelope'
]

publish()
