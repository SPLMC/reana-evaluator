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


def plot_aggregate(all_stats, prop, label, criterion, path_placer, plot_infinity=True, log=True, limit_padding=1.1):
    plt.figure()
    if log:
        plt.yscale('log')
    plt.ylabel(label)

    if criterion == 'features':
        keys = [
                "Email",
                "Lift",
                "MinePump",
                "BSN",
                "Cloud",
                "TankWar"
                ]
    elif criterion == 'configurations':
        keys = [
                "Email",
                "MinePump",
                "BSN",
                "Lift",
                "Cloud",
                "TankWar"
                ]
    max_means = 0

    for strategy in all_stats.get_strategies():
        stats_by_strategy = all_stats.get_stats_by_strategy(strategy)
        props = list()
        for key in keys:
            stats = stats_by_strategy.get(key)
            if stats is not None:
                props.append(stats_to_list(prop, stats))
            else:
                props.append(None)

        means = list()
        devs = list()
        for values in props:
            if values is not None:
                mean = numpy.mean(values)
                means.append(mean)
                max_means = max(max_means, mean)
                devs.append(numpy.std(values))
            else:
                means.append(10E15 if plot_infinity else numpy.inf)
                devs.append(numpy.nan)

        plt.errorbar(range(1,len(keys)+1),
                 means,
                 label=strategy,
                 #yerr=devs,
                 marker='o')
                 #numpy.ma.masked_invalid(means))

    plt.xticks(range(1, len(keys)+1),
               keys,
               #rotation=45
               )
    plt.legend(loc='lower left', ncol=2, bbox_to_anchor=(0, 1.02))
    plt.axis([0.7, 6.3, 10, max_means*limit_padding])

    plt.savefig(path_placer('mean-'+prop+'-'+criterion+'_ascending-'+('logarithmic-' if log else '')+'ALL.png'),
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
