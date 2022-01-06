# -*- coding: utf-8 -*-

"""spear2sc.spear_utils: Utitlity methods to read SPEAR files"""


def process_line(line):
    """ (list of str) -> list of list of float

    Parses line, a line of time, frequency and amplitude data output by
    SPEAR in the 'text - partials' format.
    Returns a list of timepoints. Each timepoint is a list of floats
    in the form: [<time in s>, <frequency in Hz>, <amplitude 0.0-1.0>]

    >>> process_line('0.145 443.309723 0.112565 0.1575 443.597656 0.124895')
    [[0.145, 443.309723, 0.112565], [0.1575, 443.597656, 0.124895]]

    """
    partial = []

    split_line = line.strip().split()
    while len(split_line) > 0:
        time_point = []
        for i in range(3):
            item = float(split_line.pop(0))
            time_point.append(item)
        partial.append(time_point)

    return partial


index_time = 0
index_freq = 1
index_amp = 2


def get_durations(partial):
    """Converts partial's absolute time offsets into durations

    Note, that the size of duration's list is one element smaller than partial's entry count

    :param partial: Sound partial, [<time in s>, <frequency in Hz>, <amplitude 0.0-1.0>]
    :type partial: list
    :return: A list of partial's duration, e.g. partial's time envelope
    :rtype: list
    """
    res = []
    for x in range(1, len(partial)):
        res.append((partial[x][index_time] - partial[x - 1][index_time]))
    return res
