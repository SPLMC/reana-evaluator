# coding=utf-8
from numpy import mean
from scipy.stats import *
import itertools

from plotter import *


SIGNIFICANCE = 0.05
NORMALITY_TEST = normaltest
#NORMALITY_TEST = shapiro


def descriptive_analysis(all_stats):
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
            boxplot_property(stats_by_spl,
                             spl+"-logarithmic",
                             prop,
                             path_placer=in_results,
                             log=True)

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
            boxplot_property(stats_by_strategy,
                             strategy+"-logarithmic",
                             prop,
                             path_placer=in_results,
                             log=True)


def test_hypotheses(all_stats):
    spls = all_stats.get_spls()
    stats = {spl: all_stats.get_stats_by_spl(spl) for spl in spls}
    aggregated_details = {}
    for spl, stats_by_strategy in stats.iteritems():
        time_by_strategy = {strategy: stats_to_list("time", stat_list)
                                for strategy, stat_list in stats_by_strategy.iteritems()}
        details = _test_spl_time(spl, time_by_strategy)
        aggregated_details[spl] = details
    import pprint
    pprint.pprint(aggregated_details, indent=2)


def _test_spl_time(spl, time_by_strategy):
    print "Testing for", spl
    time_samples = time_by_strategy.values()
    strategies = time_by_strategy.keys()
    pairs = itertools.combinations(strategies, 2)
    aggregated_details = {}
    for pair in pairs:
        strat1, strat2 = pair
        print "\t", strat1, "X", strat2
        sample1 = time_by_strategy[strat1]
        sample2 = time_by_strategy[strat2]

        result, details = _compare_samples(sample1, sample2)
        if result < 0:
            print "\t\t", strat2, "is significantly higher."
        elif result > 0:
            print "\t\t", strat1, "is significantly higher."
        else:
            print "\t\t", strat1, "==", strat2
        
        aggregated_details[pair] = details
    return aggregated_details


def _compare_samples(sample1, sample2):
    '''
    Returns -1 if sample2 is higher, +1 if sample1 is higher or 0 if they are
    not significantly different.
    '''
    mean1 = mean(sample1)
    mean2 = mean(sample2)

    if not _is_normally_distributed(sample1) or not _is_normally_distributed(sample2):
        normality = "Not all are normal"
        are_equal, details = _non_normal_are_equal(sample1, sample2)
    else:
        normality = "All are normal"
        are_equal, details = _normal_are_equal(sample1, sample2)

    if not are_equal:
        result = mean1 - mean2
    else:
        result = 0
    aggregated_details = (normality,
                          details,
                          {"mean 1": mean1,
                           "mean 2": mean2})
    
    return result, aggregated_details


def _map_values(a_dict, mapper):
    return {key: mapper(value) for key, value in a_dict.iteritems()}


def _is_normally_distributed(sample):
    w, p = normaltest(sample)
    return p >= SIGNIFICANCE


def _non_normal_are_equal(sample1, sample2):
    u, p = mannwhitneyu(sample1,
                        sample2,
                        use_continuity=False)
    return p >= SIGNIFICANCE, ("Mann-Whitney", {"U": u, "p-value": p})


def _normal_are_equal(sample1, sample2):
    equal_vars = _variances_are_equal(sample1, sample2)
    are_equal, details = _test_normal_equality(sample1, sample2, equal_vars)
    return are_equal, details

def _variances_are_equal(sample1, sample2):
    stat, p = bartlett(sample1, sample2)
    return p >= SIGNIFICANCE

def _test_normal_equality(sample1, sample2, equal_variances):
    stat, p = ttest_ind(sample1, sample2, equal_var=equal_variances)
    method = "T-test" if equal_variances else "Welch"
    return p >= SIGNIFICANCE, (method, {"statistic": stat, "p-value": p})