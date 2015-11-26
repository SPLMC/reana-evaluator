#!/usr/bin/env python
# coding=utf-8

import os
import os.path
import re
import simplejson as json
import subprocess

import numpy
import matplotlib.pyplot as plt


REANA_ROOT = "/home/thiago/Projects/workspace/reana/"
PARAM_PATH = "/home/thiago/Projects/param/param"

CLASSPATH = ":".join([os.path.join(REANA_ROOT, "bin"),
                      os.path.join(REANA_ROOT, "libs/*")])
REANA_MAIN = "java -Xss100m -cp "+CLASSPATH+" ui.CommandLineInterface --all-configurations --stats --param-path="+PARAM_PATH

REANA_ARGS = {"Feature-family-based": "--analysis-strategy=FEATURE_FAMILY",
              "Feature-product-based": "--analysis-strategy=FEATURE_PRODUCT",
              "Product-based": "--analysis-strategy=PRODUCT",
              "Family-based": "--analysis-strategy=FAMILY",
              "Family-product-based": "--analysis-strategy=FAMILY_PRODUCT"}

NUMBER_OF_RUNS = 20


class Stats(object):
    '''
    Holder of parsed statistics.
    '''
    def __init__(self, stats_str):
        self.time = self._parse_running_time(stats_str)
        self.memory = self._parse_memory_used(stats_str)
        self.max_formula_size = self._parse_max_formula_size(stats_str)
        self.min_formula_size = self._parse_min_formula_size(stats_str)
        self.all_formulae_sizes = self._parse_all_formulae_sizes(stats_str)

    @property
    def mean_formula_size(self):
        try:
            return float(sum(self.all_formulae_sizes))/len(self.all_formulae_sizes)
        except TypeError as e:
            print "Problem with formulae sizes: ", self.all_formulae_sizes
            return 0.0

    def _parse_running_time(self, stats_str):
        pattern = re.compile(r"Total running time: (\d+) ms\n")
        matched = pattern.search(stats_str).group(1)
        return int(matched)

    def _parse_memory_used(self, stats_str):
        pattern = re.compile(r"Maximum memory used: (\d+\.?\d*) MB\n")
        matched = pattern.search(stats_str).group(1)
        return float(matched)

    def _parse_min_formula_size(self, stats_str):
        pattern = re.compile(r"Minimum formula size: (\d+)\s*\n")
        matched = pattern.search(stats_str).group(1)
        return int(matched)

    def _parse_max_formula_size(self, stats_str):
        pattern = re.compile(r"Maximum formula size: (\d+)\s*\n")
        matched = pattern.search(stats_str).group(1)
        return int(matched)

    def _parse_all_formulae_sizes(self, stats_str):
        pattern = re.compile(r"All formulae sizes: (\[.*\])\n")
        sizes = pattern.search(stats_str).group(1)
        return json.loads(sizes)

    def __str__(self):
        info = self.__dict__.copy()
        del info["all_formulae_sizes"]
        info["mean_formula_size"] = self.mean_formula_size
        return str(info)


def get_executable(strategy):
    return REANA_MAIN + " " + REANA_ARGS[strategy]


def parse_stats(program_output):
    _, _, stats = program_output.partition("Stats:")
    return Stats(stats)


def run_for_stats(command_line):
    '''
    Runs the given executable and returns the resulting statistics.
    '''
    FNULL = open(os.devnull, 'w')
    output = subprocess.check_output(command_line,
                                     shell=True,
                                     cwd=REANA_ROOT,
                                     stderr=FNULL)
    return parse_stats(output) 

def stats_to_list(stat_name, stats_list):
    return map(lambda stats: getattr(stats, stat_name),
               stats_list)

def mean_time_with_std_dev(stats):
    times = stats_to_list("time", stats)
    return (numpy.mean(times), numpy.std(times))


def plot_time(stats):
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
    plt.show()


if __name__ == '__main__':
    stats = {}
    for strategy in REANA_ARGS:
        print strategy
        print "---------"
        command_line = get_executable(strategy)
        #temp_stats = [run_for_stats(command_line) for i in xrange(NUMBER_OF_RUNS)]
        temp_stats = list()
        for i in xrange(NUMBER_OF_RUNS):
            temp_stat = run_for_stats(command_line)
            temp_stats.append(temp_stat)
            print temp_stat
        stats[strategy] = temp_stats
        #for stat in temp_stats:
        #    print stat
        print "==========================================================="

    plot_time(stats)
