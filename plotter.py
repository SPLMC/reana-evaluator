# coding=utf-8
import numpy
import matplotlib.pyplot as plt
from collections import OrderedDict


def stats_to_list(stat_name, stats_list):
    return map(lambda stats: getattr(stats, stat_name),
               stats_list)

def mean_time_with_std_dev(stats):
    times = stats_to_list("analysis_time", stats)
    return (numpy.mean(times), numpy.std(times))


def plot_time(stats, name, path_placer=lambda path: path):
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

    plt.yscale('log')
    plt.bar(index, times, bar_width,
            color='y',
            yerr=std_devs)
    plt.xticks(index + bar_width/2, keys)
    plt.ylabel("Mean time (ms)")
    plt.savefig(path_placer('mean-analysis-time-logarithmic-'+name+'.png'),
                format="png",
                bbox_inches="tight")
    plt.close()


def boxplot_property(stats,
                     target_name,
                     property_name,
                     path_placer=lambda path: path,
                     log=False):
    data = OrderedDict()
    for key, stats in stats.iteritems():
        data[key] = stats_to_list(property_name, stats)
    _boxplot_base(data,
                  target_name,
                  property_name,
                  path_placer,
                  log)


def _boxplot_base(data,
                  target_name,
                  property_name,
                  path_placer=lambda path: path,
                  log=False):
    plt.figure(num=1,figsize=(18,10),dpi=80)

    plots = data.values()
    if log:
        plt.yscale('log')
    plt.boxplot(plots)
    plt.xticks(range(1, len(plots)+1),
               data.keys(),
               rotation=45)

    plt.savefig(path_placer('boxplot-'+property_name+'-'+target_name+'.png'),
                format="png",
                bbox_inches="tight")
    plt.close()
