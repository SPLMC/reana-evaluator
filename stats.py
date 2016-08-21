# coding=utf-8
from collections import OrderedDict
import numpy
from configurations import SPL_ORDER,ANALYSIS_STRATEGIES 

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
        indexed=OrderedDict()
        for spl in SPL_ORDER:
            for stats in self.data:
                if (stats.strategy == strategy and stats.spl == spl):
                    indexed.update({stats.spl: stats.data}) 
               
        return indexed

    def get_stats_by_spl(self, spl):
        '''
        Returns all stats for the given SPL, indexed by
        the analysis strategy.
        '''
        
        indexed=OrderedDict()
        for strategy in ANALYSIS_STRATEGIES:
            for stats in self.data:
                if (stats.strategy == strategy and stats.spl == spl):
                    indexed.update({stats.strategy: stats.data}) 
               
        return indexed
        
        


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
                       inner_memory,
                       max_formula_size,
                       min_formula_size,
                       all_formulae_sizes,
                       all_model_checking_times=None,
                       elapsed_model_checking_time=numpy.nan,
                       elapsed_expression_solving_time=numpy.nan):
        self.total_time = total_time
        self.analysis_time = analysis_time
        self.memory = memory
        self.inner_memory = inner_memory or memory
        self.max_formula_size = max_formula_size
        self.min_formula_size = min_formula_size
        self.all_formulae_sizes = all_formulae_sizes
        self.all_model_checking_times = all_model_checking_times
        self.elapsed_model_checking_time = elapsed_model_checking_time
        self.elapsed_expression_solving_time = elapsed_expression_solving_time

    @property
    def mean_formula_size(self):
        try:
            return float(sum(self.all_formulae_sizes))/len(self.all_formulae_sizes)
        except TypeError as e:
            print "Problem with formulae sizes: ", self.all_formulae_sizes
            return 0.0

    @property
    def mean_model_checking_time(self):
        try:
            return numpy.mean(self.all_model_checking_times)
        except TypeError as e:
            print "Problem with model checking times: ", self.all_model_checking_times
            return 0.0

    @property
    def sequential_model_checking_time(self):
        try:
            return sum(self.all_model_checking_times)
        except TypeError as e:
            print "Problem with model checking times: ", self.all_model_checking_times
            return 0.0

    def __str__(self):
        info = self.__dict__.copy()
        del info["all_formulae_sizes"]
        del info["all_model_checking_times"]
        info["mean_formula_size"] = self.mean_formula_size
        info["mean_model_checking_time"] = self.mean_model_checking_time
        return str(info)
