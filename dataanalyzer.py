# coding=utf-8
from numpy import mean
from scipy.stats import *
import itertools
import pprint

from plotter import *

SIGNIFICANCE = 0.01
NORMALITY_TEST = normaltest
#NORMALITY_TEST = shapiro


def descriptive_analysis(all_stats, path_placer=lambda path: path):
    criterion='configurations'
    #for criterion in ['features', 'configurations']:
        
    plot_aggregate_barplots(all_stats, "analysis_time", "Analysis time (ms)", criterion, path_placer, plot_infinity=False, limit_padding=1.2, log=True)
    plot_aggregate_barplots(all_stats, "memory", "Peak memory (MB)", criterion, path_placer, plot_infinity=False, log=False)
    plot_aggregate_boxplots(all_stats, "analysis_time", "Analysis time (ms)", criterion, path_placer, plot_infinity=False, limit_padding=1.2, log=True, minimum=0.1)
    plot_aggregate_boxplots(all_stats, "memory", "Peak memory (MB)", criterion, path_placer, plot_infinity=False, log=False)
    plot_aggregate_barplots(all_stats, "elapsed_model_checking_time", "Model checking time (ms)", criterion, path_placer, plot_infinity=False, log=False)
    plot_aggregate_barplots(all_stats, "elapsed_expression_solving_time", "Expression solving time (ms)", criterion, path_placer, plot_infinity=False, log=False)
    plot_aggregate_barplots(all_stats, "elapsed_model_checking_time", "Model checking time (ms)", criterion, path_placer, plot_infinity=False, log=True)
    plot_aggregate_barplots(all_stats, "elapsed_expression_solving_time", "Expression solving time (ms)", criterion, path_placer, plot_infinity=False, log=True)
        
       
        
    plot_aggregate(all_stats, "analysis_time", "Analysis time (ms)", criterion, path_placer, plot_infinity=False, limit_padding=1.6)
    plot_aggregate(all_stats, "total_time", "Total time (ms)", criterion, path_placer, plot_infinity=False, limit_padding=1.6)
    plot_aggregate(all_stats, "memory", "Peak memory (MB)", criterion, path_placer, plot_infinity=False, log=False)
    plot_aggregate(all_stats, "elapsed_model_checking_time", "Model checking time (ms)", criterion, path_placer, plot_infinity=False, log=False)

        

    props = ["analysis_time",
             "memory"]

    for spl in all_stats.get_spls():
        stats_by_spl = all_stats.get_stats_by_spl(spl)
        if(len(stats_by_spl)>0):
            plot_time(stats_by_spl,
                  spl,
                  path_placer)
            for prop in props:
                boxplot_property(stats_by_spl,
                             spl,
                             prop,
                             path_placer)
                boxplot_property(stats_by_spl,
                             spl+"-logarithmic",
                             prop,
                             path_placer,
                             log=True)

    for strategy in all_stats.get_strategies():
        stats_by_strategy = all_stats.get_stats_by_strategy(strategy)
        if(len(stats_by_strategy)>0):
            plot_time(stats_by_strategy,
                      strategy,
                      path_placer)
            for prop in props:
                boxplot_property(stats_by_strategy,
                             strategy,
                             prop,
                             path_placer)
                boxplot_property(stats_by_strategy,
                             strategy+"-logarithmic",
                             prop,
                             path_placer,
                             log=True)


def test_hypotheses(all_stats):
    spls = all_stats.get_spls()
    stats = {spl: all_stats.get_stats_by_spl(spl) for spl in spls}
    for stat_name in ["analysis_time", "memory"]:
        print "==============================="
        print stat_name
        print "-------------------------------"
        aggregated_details = {}
        for spl, stats_by_strategy in stats.iteritems():
            print "Testing", stat_name,"for", spl
            details = _test_spl_stat(spl,
                                     stats_by_strategy,
                                     stat_name)
            aggregated_details[spl] = details
        pprint.pprint(aggregated_details, indent=2)
       

def _test_spl_stat(spl, stats_by_strategy, stat_name):
    samples_by_strategy = {strategy: stats_to_list(stat_name, stat_list)
                            for strategy, stat_list in stats_by_strategy.iteritems()}

    strategies = samples_by_strategy.keys()
    pairs = itertools.combinations(strategies, 2)
    aggregated_details = {}
    for pair in pairs:
        strat1, strat2 = pair
        sample1 = samples_by_strategy[strat1]
        sample2 = samples_by_strategy[strat2]

        error = None
        if len(sample1) < 8:
            error = strat1
        elif len(sample2) < 8:
            error = strat2

        if error is not None:
            print "\tStrategy %s has not enough samples. Skipping..." % error
            continue

        result, details = _compare_samples(sample1, sample2)
        if result == 0:
            print "\t", strat1, "and", strat2, "are not significantly different"
        
        aggregated_details[pair] = details

    means = {strategy: mean(samples_by_strategy[strategy]) for strategy in strategies}
    ordered = sorted(means.items(), key=lambda item: item[1])
    print "\t", " < ".join(map(str,ordered))
    return aggregated_details


def _compare_samples(sample1, sample2):
    '''
    Returns -1 if sample2 is higher, +1 if sample1 is higher or 0 if they are
    not significantly different.
    '''
    mean1 = mean(sample1)
    mean2 = mean(sample2)
    gain = max(mean1, mean2)/min(mean1, mean2)

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
                           "mean 2": mean2,
                           "gain": str(gain) + "x"})
    
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
