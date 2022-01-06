# -*- coding: utf-8 -*-

import numpy as np
import plotille

from .spear_utils import index_time, index_amp

"""spear2sc.analysis A set of methods to perform basic analysis of the partials"""


def get_durations_thresh(partials):
    """Gets the 92th percentile of partial durations

    The concrete percentile threshold is sort of an empirical value

    :param partials: list of sound partials
    :type partials: list
    :return: 92th percentile of partials durations
    :rtype: float
    """
    durations = list(map(lambda p: get_total_duration(p), partials))
    return np.percentile(durations, 92)


def get_amp_thresh(partials, est_dur_thresh):
    """Get the 30th percentile of partial's levels

    Only those partials which are longer than est_dur_thresh are counted.
    The concrete percentile threshold is sort of an empirical value

    :param partials: list of sound partials
    :type partials: list
    :param est_dur_thresh: duration threshold, seconds
    :type est_dur_thresh: float
    :return: 30th percentile of partial's levels
    :rtype: float
    """
    return np.percentile(list(map(lambda p: get_amp_mean(p), filter(lambda p: get_total_duration(p) > est_dur_thresh, partials))), 30)


def get_amp_mean(partial):
    """Gets the median (50th percentile) of partial's levels

    :param partial: sound partial (list of [time, freq, amp] points)
    :type partial: list
    :return: median of of partial's levels
    :rtype: float
    """
    return np.percentile(list(map(lambda p: p[index_amp], partial)), 50)


def get_total_duration(partial):
    """Gets the total duration of a partial in seconds
    :param partial: sound partial (list of [time, freq, amp] points)
    :type partial: list
    :return: Duration of a partials in seconds
    :rtype: float
    """
    return partial[len(partial) - 1][index_time] - partial[0][index_time]


def get_amp_envelope(partial):
    """Retrieves particle's level envelope over time

    :param partial: sound partial (list of [time, freq, amp] points)
    :type partial: list
    :return: Tuple of timestamps and levels for plotting
    :rtype tuple(list, list)
    """
    return list(map(lambda p: p[index_time], partial)), list(map(lambda p: p[index_amp], partial))


def print_analysis(partials, options):
    """Prints partials analysis results to stdout

    This analysis includes: estimating the number of partials, possible estimating
    durations and level thresholds, if they are not specified in options.
    If graphics is True in options, also prints the graphs

    :param partials: list of sound partials
    :type partials: list
    :param options: Analysis options (est_duration_thresh, est_level_thresh, graphics)
    :type options: tuple(float, float, boolean)
    :return:
    """
    est_duration_thresh, est_level_thresh, graphics = options
    if est_duration_thresh is None:
        est_duration_thresh = get_durations_thresh(partials)
    if est_level_thresh == 0.0:
        est_level_thresh = get_amp_thresh(partials, est_duration_thresh)

    print("92th percentile of durations is: {:10.4f}".format(est_duration_thresh))
    print("30th percentile of levels is: {:10.4f}".format(est_level_thresh))
    est_num_partials = 0

    fig = plotille.Figure()
    fig.color_mode = 'byte'
    fig.width = 120
    fig.height = 30

    partials_total = 0
    for partial in partials:
        partials_total = partials_total + 1
        if get_total_duration(partial) > est_duration_thresh and get_amp_mean(partial) > est_level_thresh:
            est_num_partials = est_num_partials + 1
            x, y = get_amp_envelope(partial)
            fig.plot(x, y)
    if graphics:
        print(fig.show())
    print("Total number of partials: {}".format(partials_total))
    print("Estimated number of representative partials: {} ({:6.2f}%)"
          .format(est_num_partials, est_num_partials / (partials_total + 0.001) * 100))