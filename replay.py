# coding=utf-8
'''
Module Replay
-------------

Handles replay of previously gathered data.
'''
import json
import csv

from collections import defaultdict

from stats import AllStats, CummulativeStats, Stats
from configurations import AVAILABLE_SPL

def load(filename):
    '''
    Loads data for replay.

    :return: AllStats
    '''
    with open(filename, 'r') as source:
        contents = source.read()
        raw_data = json.loads(contents)
        return AllStats(_parse_stats(raw_data))


def save(all_stats, filename):
    '''
    Save data for later replay.

    :type all_stats: AllStats
    '''
    
    raw_data = _dump_cummulative_stats(all_stats.data)
    with open(filename, 'w') as dest:
        dest.write(json.dumps(raw_data))


def _parse_stats(raw_data):
    '''
    Converts stats in dict format to a list of CummulativeStats.
    '''
    stats = list()
    for spl in raw_data:
        for strategy in raw_data[spl]:
            data = raw_data[spl][strategy]
            stats.append(CummulativeStats(spl,
                                          strategy,
                                          map(lambda stats: Stats(**stats),
                                              data)))
    return stats


def _dump_cummulative_stats(stats):
    '''
    Converts a list of CummulativeStats to a dict of stats.
    '''
    dumped = defaultdict(lambda: defaultdict(list))
    for s in stats:
        data = map(_dump_single_stats, s.data)
        dumped[s.spl][s.strategy].extend(data)
    return dumped


def _dump_single_stats(stats):
    '''
    Converts a Stats object to a dict.
    '''
    return stats.__dict__
def generate_csv(all_stats, data_file):
    '''
    Generates a cvs file from replay
    '''
    print "Generating csv file from replay"
    f = csv.writer(open(data_file, "wb+"))
    f.writerow([AVAILABLE_SPL[list(AVAILABLE_SPL)[0]].factor1_name,AVAILABLE_SPL[list(AVAILABLE_SPL)[0]].factor2_name,"strategy","spl", "time", "memory"])
  
        
    spls = all_stats.get_spls()
    
    stats = {spl: all_stats.get_stats_by_spl(spl) for spl in spls}
    for spl, stats_by_strategy in stats.iteritems():
        for strategy,replays in stats_by_strategy.items():
            for details in replays:
                    
                    
                    f.writerow([AVAILABLE_SPL[spl].factor1_level,AVAILABLE_SPL[spl].factor2_level,strategy,spl, details.analysis_time, details.memory])
    return data_file
