#!/usr/bin/env python
# coding=utf-8

from dataanalyzer import descriptive_analysis, test_hypotheses
from runner import run_all_analyses, run_r_script
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
        all_stats = replay.load(in_results("replay.json"))

    descriptive_analysis(all_stats, path_placer=in_results)
    test_hypotheses(all_stats)
    data_file=os.getcwd()+"/"+RESULTS_DIR+"/data.csv"
    data_file=replay.generate_csv(all_stats,data_file)
    run_r_script(os.getcwd()+"/"+RESULTS_DIR,data_file)                
    
