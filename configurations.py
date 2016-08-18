# coding=utf-8

import os.path
from collections import namedtuple, OrderedDict
from itertools import product


__all__ = ['CONFIGURATIONS',
           'CWD']


TOOLS_PATH = "tools"
REANA_ROOT = TOOLS_PATH
PARAM_PATH = os.path.join(TOOLS_PATH, "param")
MODELS_PATH = "models"
CWD = '.'

JAR = os.path.join(REANA_ROOT, "reana-spl.jar")
REANA_MAIN = "java -Xss100m -jar "+JAR+" --all-configurations --suppress-report --stats --param-path="+PARAM_PATH

ANALYSIS_STRATEGIES =OrderedDict()
with open("analysis_strategies") as fp:
     
     for line in fp:
        
        if(len(line.split(",", 8))>=2):
            ANALYSIS_STRATEGIES[line.split(",", 4)[0]]= line.split(",", 4)[1]
              

SPL = namedtuple("SPL", ["uml_model", "feature_model","factor1_name","factor1_level","factor2_name","factor2_level"])

SPL_ORDER=[]
AVAILABLE_SPL={}

with open("available_spl") as fp:
     
     
     
     for line in fp:
        if(len(line.split(",", 8))>=8):
            AVAILABLE_SPL[line.split(",", 8)[0]]=SPL(uml_model= line.split(",",8)[1], feature_model=line.split(",", 8)[2],factor1_name=line.split(",", 8)[3],factor1_level=line.split(",", 8)[4],factor2_name=line.split(",", 8)[5],factor2_level=line.split(",", 8)[6])
            SPL_ORDER.append(line.split(",", 8)[0])
        elif(len(line.split(",", 8))>=4):
            AVAILABLE_SPL[line.split(",", 8)[0]]=SPL(uml_model= line.split(",",8)[1], feature_model=line.split(",", 8)[2],factor1_name='',factor1_level='',factor2_name='',factor2_level='')    
            SPL_ORDER.append(line.split(",", 8)[0])    
    
#AVAILABLE_SPL = {
#        "BSN": SPL(uml_model="BSN_models_without_File.xml",
#                   feature_model="BSN-FM_without_file.txt"),
#        "Email": SPL(uml_model="Email.xml",
#                     feature_model="email-FM.txt"),
#        "Cloud": SPL(uml_model="CloudComputing.xml",
#                     feature_model="CNF_CloudComputing.txt"),
#        "Lift": SPL(uml_model="LiftSystem.xml",
#                    feature_model="CNF_LiftSystem.txt"),
#        "MinePump": SPL(uml_model="MinePump.xml",
#                        feature_model="CNF_MinePump.txt"),
        
#    }

print AVAILABLE_SPL
def get_arg_for_strategy(strategy):
    return "--analysis-strategy="+ANALYSIS_STRATEGIES[strategy]


def get_arg_for_spl(spl):
    spl = AVAILABLE_SPL[spl]
    return ("--feature-model=" + os.path.join(MODELS_PATH, spl.feature_model) + " " +
            "--uml-model=" + os.path.join(MODELS_PATH, spl.uml_model))


def get_executable(strategy, spl):
    '''
    Returns the corresponding executable for the given analysis configuration.
    '''
    return ("/usr/bin/time -v " + REANA_MAIN + " "
            + get_arg_for_strategy(strategy) + " "
            + get_arg_for_spl(spl))


CONFIGURATIONS= OrderedDict()
for strategy in ANALYSIS_STRATEGIES:
    for spl in SPL_ORDER:
        CONFIGURATIONS.update({(spl, strategy): get_executable(strategy, spl)})

# These 3 take a long time to run (between 1.5 and 3.5 hours), so it is best
#to run them separately and then merge the results in replay.json.

#CONFIGURATIONS = {
#        ("MinePump", "Family-based"): get_executable("Family-based", "MinePump"),
#        ("MinePump", "Family-product-based"): get_executable("Family-product-based", "MinePump"),
#        ("Cloud", "Product-based"): get_executable("Product-based", "Cloud")
#   }
