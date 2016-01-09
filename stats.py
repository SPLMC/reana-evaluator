# coding=utf-8
from collections import OrderedDict


class AllStats(object):
    '''
    Set of all gathered stats.
    '''

    def __init__(self, cummulative_stats):
        self.data = cummulative_stats

    def get_spls(self):
        return set([stats.spl for stats in self.data])

    def get_strategies(self):
        return set([stats.strategy for stats in self.data])

    def get_stats_by_strategy(self, strategy):
        '''
        Returns all stats for the given strategy, indexed by
        the analyzed SPL.
        '''
        indexed = {stats.spl: stats.data for stats in self.data
                    if stats.strategy == strategy}
        return OrderedDict(sorted(indexed.items()))

    def get_stats_by_spl(self, spl):
        '''
        Returns all stats for the given SPL, indexed by
        the analysis strategy.
        '''
        indexed = {stats.strategy: stats.data for stats in self.data
                    if stats.spl == spl}
        return OrderedDict(sorted(indexed.items()))


class CummulativeStats(object):
    '''
    Cummulative stats for a given SPL and a given strategy.
    '''
    def __init__(self, spl, strategy, data):
        '''
        :type spl: str
        :type strategy: str
        :type data: list of Stats
        '''
        self.spl = spl
        self.strategy = strategy
        self.runs = len(data)
        self.data = data


class Stats(object):
    '''
    Holder of parsed statistics for a single ReAna run.
    '''
    def __init__(self, total_time,
                       analysis_time,
                       memory,
                       max_formula_size,
                       min_formula_size,
                       all_formulae_sizes):
        self.total_time = total_time
        self.analysis_time = analysis_time
        self.memory = memory
        self.max_formula_size = max_formula_size
        self.min_formula_size = min_formula_size
        self.all_formulae_sizes = all_formulae_sizes

    @property
    def mean_formula_size(self):
        try:
            return float(sum(self.all_formulae_sizes))/len(self.all_formulae_sizes)
        except TypeError as e:
            print "Problem with formulae sizes: ", self.all_formulae_sizes
            return 0.0

    def __str__(self):
        info = self.__dict__.copy()
        del info["all_formulae_sizes"]
        info["mean_formula_size"] = self.mean_formula_size
        return str(info)
