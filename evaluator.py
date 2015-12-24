#!/usr/bin/env python
# coding=utf-8

from runner import run_all_analyses
import replay

import argparse
import os
import numpy
import matplotlib.pyplot as plt

from datetime import datetime

inResults = lambda filename: os.path.join(RESULTS_DIR, filename)

def stats_to_list(stat_name, stats_list):
    return map(lambda stats: getattr(stats, stat_name),
               stats_list)

def mean_time_with_std_dev(stats):
    times = stats_to_list("time", stats)
    return (numpy.mean(times), numpy.std(times))


def plot_time(stats, name):
    plt.figure(num=1,figsize=(18,10),dpi=80)

    bar_width = 0.35
    keys = stats.keys()
    index = numpy.arange(len(keys))
    times = list()
    std_devs = list()
    for key in keys:
        stat = stats[key]
        mean_time, std_dev = mean_time_with_std_dev(stat)
        times.append(mean_time)
        std_devs.append(std_dev)

    plt.bar(index, times, bar_width,
            color='y',
            yerr=std_devs,
            label="Strategies")
    plt.xticks(index + bar_width/2, keys)
    plt.xlabel("Strategy")
    plt.ylabel("Mean time (ms)")
    plt.legend()
    plt.savefig(inResults('mean-runtime-'+name+'.png'),
                format="png",
                bbox_inches="tight")
    #plt.show()

def _parse_args():
    '''
    Parses command-line args.

    Return object:
        - num_runs: the number of runs for each SPL-strategy pair (if
            not replaying).
        - replay_dir: the directory in which the replay data is stored,
            or None if not in replay mode.
    '''
    parser = argparse.ArgumentParser(description="Run ReAna's strategies for a number of SPLs.")
    parser.add_argument('--replay',
                        dest='replay_dir',
                        action='store',
                        help="Enters replay mode, using the given directory")
    parser.add_argument('--runs',
                        dest='num_runs',
                        action='store',
                        type=int,
                        default=1,
                        help="Number of runs for each SPL-strategy pair (default: %(default)s)")
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()

    if args.replay_dir is None:
        RESULTS_DIR = "results-"+ datetime.now().isoformat()
        os.mkdir(RESULTS_DIR)
        all_stats = run_all_analyses(args.num_runs)
        replay.save(all_stats, inResults("replay.json"))
    else:
        RESULTS_DIR = args.replay_dir
        print RESULTS_DIR, type(RESULTS_DIR)
        all_stats = replay.load(inResults("replay.json"))

    for spl in all_stats.get_spls():
        plot_time(all_stats.get_stats_by_spl(spl), spl)

    for strategy in all_stats.get_strategies():
        plot_time(all_stats.get_stats_by_strategy(strategy), strategy)
