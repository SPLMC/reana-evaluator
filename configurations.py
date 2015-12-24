# coding=utf-8

import os.path

from collections import namedtuple
from itertools import product


__all__ = ['CONFIGURATIONS',
           'CWD']


REANA_ROOT = "/home/thiago/Projects/workspace/reana/"
PARAM_PATH = "/home/thiago/Projects/param/param"
CWD = REANA_ROOT

CLASSPATH = ":".join([os.path.join(REANA_ROOT, "bin"),
                      os.path.join(REANA_ROOT, "libs/*")])
REANA_MAIN = "java -Xss100m -cp "+CLASSPATH+" ui.CommandLineInterface --all-configurations --stats --param-path="+PARAM_PATH

ANALYSIS_STRATEGIES = {
        "Feature-family-based": "FEATURE_FAMILY",
        "Feature-product-based": "FEATURE_PRODUCT",
        "Product-based": "PRODUCT",
        "Family-based": "FAMILY",
        "Family-product-based": "FAMILY_PRODUCT"
    }


SPL = namedtuple("SPL", ["uml_model", "feature_model"])

AVAILABLE_SPL = {
        "BSN": SPL(uml_model="BSN_models_without_File.xml",
                   feature_model="BSN-FM_without_file.txt"),
        "Email": SPL(uml_model="Email.xml",
                     feature_model="email-FM.txt"),
        "Cloud": SPL(uml_model="CloudComputing.xml",
            feature_model="CNF_CloudComputing.txt"),
        "Lift": SPL(uml_model="LiftSystem.xml",
                    feature_model="CNF_LiftSystem.txt"),
        "MinePump": SPL(uml_model="MinePump.xml",
            feature_model="CNF_MinePump.txt"),
    }


def get_arg_for_strategy(strategy):
    return "--analysis-strategy="+ANALYSIS_STRATEGIES[strategy]


def get_arg_for_spl(spl):
    spl = AVAILABLE_SPL[spl]
    return ("--feature-model=" + spl.feature_model + " " +
            "--uml-model="+spl.uml_model)


def get_executable(strategy, spl):
    '''
    Returns the corresponding executable for the given analysis configuration.
    '''
    return (REANA_MAIN + " "
            + get_arg_for_strategy(strategy) + " "
            + get_arg_for_spl(spl))


CONFIGURATIONS = {(spl, strategy): get_executable(strategy, spl)
        for strategy, spl in product(ANALYSIS_STRATEGIES, AVAILABLE_SPL)}
