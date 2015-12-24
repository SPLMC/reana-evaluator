# coding=utf-8
import os
import re
import simplejson as json
import subprocess

from configurations import CONFIGURATIONS, CWD
from stats import AllStats, CummulativeStats, Stats


def run_all_analyses(number_of_runs):
    '''
    Runs all analyses for all SPLs and returns an AllStats object.
    '''
    all_stats = []
    for (spl, strategy), command_line in CONFIGURATIONS.iteritems():
        name = strategy + " ("+spl+")"
        print name
        print "---------"
        stats = run_analysis(spl, strategy, command_line, number_of_runs)
        all_stats.append(stats)
        print "===================================="
    return AllStats(all_stats)


def run_analysis(spl, strategy, command_line, number_of_runs):
    data = [_run_for_stats(command_line) for i in xrange(number_of_runs)]
    return CummulativeStats(spl, strategy, data)


def _run_for_stats(command_line):
    '''
    Runs the given executable and returns the resulting statistics.
    '''
    FNULL = open(os.devnull, 'w')
    output = subprocess.check_output(command_line,
                                     shell=True,
                                     cwd=CWD,
                                     stderr=FNULL)
    return _parse_stats(output) 


def _parse_stats(program_output):
    _, _, stats_str = program_output.partition("Stats:")

    time = _parse_running_time(stats_str)
    memory = _parse_memory_used(stats_str)
    max_formula_size = _parse_max_formula_size(stats_str)
    min_formula_size = _parse_min_formula_size(stats_str)
    all_formulae_sizes = _parse_all_formulae_sizes(stats_str)

    return Stats(time,
                 memory,
                 max_formula_size,
                 min_formula_size,
                 all_formulae_sizes)

def _parse_running_time(stats_str):
    pattern = re.compile(r"Total running time: (\d+) ms\n")
    matched = pattern.search(stats_str).group(1)
    return int(matched)

def _parse_memory_used(stats_str):
    pattern = re.compile(r"Maximum memory used: (\d+\.?\d*) MB\n")
    matched = pattern.search(stats_str).group(1)
    return float(matched)

def _parse_min_formula_size(stats_str):
    pattern = re.compile(r"Minimum formula size: (\d+)\s*\n")
    matched = pattern.search(stats_str).group(1)
    return int(matched)

def _parse_max_formula_size(stats_str):
    pattern = re.compile(r"Maximum formula size: (\d+)\s*\n")
    matched = pattern.search(stats_str).group(1)
    return int(matched)

def _parse_all_formulae_sizes(stats_str):
    pattern = re.compile(r"All formulae sizes: (\[.*\])\n")
    sizes = pattern.search(stats_str).group(1)
    return json.loads(sizes)
