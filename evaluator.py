#!/usr/bin/env python
# coding=utf-8

from runner import run_all_analyses
from plotter import *
import replay

import argparse
import os

from datetime import datetime

in_results = lambda filename: os.path.join(RESULTS_DIR, filename)


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
        replay.save(all_stats, in_results("replay.json"))
    else:
        RESULTS_DIR = args.replay_dir
        print RESULTS_DIR, type(RESULTS_DIR)
        all_stats = replay.load(in_results("replay.json"))

    for spl in all_stats.get_spls():
        stats_by_spl = all_stats.get_stats_by_spl(spl)
        plot_time(stats_by_spl,
                  spl,
                  path_placer=in_results)
        for prop in ["time", "memory"]:
            boxplot_property(stats_by_spl,
                             spl,
                             prop,
                             path_placer=in_results)

    for strategy in all_stats.get_strategies():
        stats_by_strategy = all_stats.get_stats_by_strategy(strategy)
        plot_time(stats_by_strategy,
                  strategy,
                  path_placer=in_results)
        for prop in ["time", "memory"]:
            boxplot_property(stats_by_strategy,
                             strategy,
                             prop,
                             path_placer=in_results)
