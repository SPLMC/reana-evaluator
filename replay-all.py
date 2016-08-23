#!/usr/bin/env python
# coding=utf-8



import argparse
import sys,os
import subprocess

from datetime import datetime

in_results = lambda filename: os.path.join(RESULTS_DIR, filename)


def _parse_args():
    '''
    Parses command-line args.

    Return object:
        - num_runs: the number of runs for each SPL-strategy pair (if
            not replaying).
        - replay_dir: the directory in which the replay data is stored,
            or None if not in replay mode.
    '''
    parser = argparse.ArgumentParser(description="Run ReAna's strategies for a number of SPLs.")
    parser.add_argument('--results',
                        dest='results',
                        action='store',
                        help="Enters replay mode, using the given directory")
    
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()

    pathname = os.path.dirname(sys.argv[0])        
    print('path =', pathname)
    BASE_DIR=args.results
    for folder in os.listdir(BASE_DIR):    
        print folder
        try:
        # Define command and arguments
        
       
            print os.getcwd()
            
            command=pathname+'/evaluator.py'
            
            args=['--replay',BASE_DIR+"/"+folder]
            # Build subprocess command
            cmd = [command]+args 
            print "Command ",cmd
        
        
            # check_output will run the command and store to result
            x = subprocess.check_output(cmd, universal_newlines=True)
            print x
            
        
        except subprocess.CalledProcessError as e:
            print 'Error'
            print e
            print e.output
            
    
        