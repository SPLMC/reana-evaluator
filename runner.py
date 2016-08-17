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
    print "@@@@", command_line
    try:
        output = subprocess.check_output(command_line,
                                         shell=True,
                                         cwd=CWD,
                                         stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print e
        print e.output
        return None
    print output
    result = _parse_stats(output)
    print result
    return result


def _parse_stats(program_output):
    _, _, stats_str = program_output.partition("Stats:")

    time = _parse_running_time(stats_str)
    analysis_time = _parse_analysis_time(stats_str)
    memory = _parse_memory_reported_by_time(stats_str)
    inner_memory = _parse_memory_used(stats_str)
    max_formula_size = _parse_max_formula_size(stats_str)
    min_formula_size = _parse_min_formula_size(stats_str)
    all_formulae_sizes = _parse_all_formulae_sizes(stats_str)
    all_model_checking_times = _parse_all_model_checking_times(stats_str)
    elapsed_model_checking_time = _parse_elapsed_model_checking_time(stats_str)
    elapsed_expression_solving_time = _parse_elapsed_expression_solving_time(stats_str)

    return Stats(time,
                 analysis_time,
                 memory,
                 inner_memory,
                 max_formula_size,
                 min_formula_size,
                 all_formulae_sizes,
                 all_model_checking_times,
                 elapsed_model_checking_time,
                 elapsed_expression_solving_time)

def _parse_running_time(stats_str):
    pattern = re.compile(r"Total running time: (\d+) ms\n")
    matched = pattern.search(stats_str).group(1)
    return int(matched)

def _parse_analysis_time(stats_str):
    pattern = re.compile(r"Total analysis time: (\d+) ms\n")
    matched = pattern.search(stats_str).group(1)
    return int(matched)

def _parse_memory_used(stats_str):
    pattern = re.compile(r"Maximum memory used: (\d+\.?\d*) MB\n")
    matched = pattern.search(stats_str).group(1)
    return float(matched)

def _parse_memory_reported_by_time(stats_str):
    pattern = re.compile(r"Maximum resident set size \(kbytes\): (\d+\.?\d*)\n")
    matched = pattern.search(stats_str).group(1)
    # Return result in MB
    return float(matched)/1024.0

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

def _parse_all_model_checking_times(stats_str):
    pattern = re.compile(r"All model checking times \(ms\): (\[.*\])\n")
    times = pattern.search(stats_str).group(1)
    return json.loads(times)

def _parse_elapsed_model_checking_time(stats_str):
    pattern = re.compile(r"Model checking time: (\d+\.?\d*) ms\n")
    matched = pattern.search(stats_str).group(1)
    return float(matched)

def _parse_elapsed_expression_solving_time(stats_str):
    pattern = re.compile(r"Expression solving time: (\d+\.?\d*) ms\n")
    mo = pattern.search(stats_str)
    if mo is not None:
        matched = mo.group(1)
        return float(matched)
    else:
        return -1.0
    
def run_r_script(RESULTS_DIR,input_file):
    'Runs R script for factorial design'
    print "Runnin R Script"
    try:
        # Define command and arguments
        
       
        
        output_file=RESULTS_DIR+"/result.txt"
        
        script_dir=os.getcwd()
        command='Rscript'
        path2script=script_dir+'/factorial-design.R'

        args=['-i',input_file,'-o',output_file,'-d',',','-v','false']
        # Build subprocess command
        cmd = [command, path2script]+args 
        print "Command ",cmd
        
        
        # check_output will run the command and store to result
        x = subprocess.check_output(cmd, universal_newlines=True)
        print x
        print 'Rscript execution finished'
       
        
    except subprocess.CalledProcessError as e:
        print 'Rscript error'
        print e
        print e.output
        return None
    