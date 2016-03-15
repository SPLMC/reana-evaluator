# coding=utf-8

import os.path

from collections import namedtuple
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
        "TankWar": SPL(uml_model="TankWar.xml",
                       feature_model="CNF_Tankwar.txt"),
    }


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


FEATURE_BASED = {(spl, strategy): get_executable(strategy, spl)
        for strategy, spl in product(["Feature-family-based", "Feature-product-based"],
                                     AVAILABLE_SPL)}
del FEATURE_BASED[("TankWar", "Feature-product-based")]

PRODUCT_BASED = {(spl, "Product-based"): get_executable("Product-based", spl)
        for spl in ["BSN", "Email", "Lift", "MinePump"]}

FAMILY_BASED = {(spl, strategy): get_executable(strategy, spl)
        for strategy, spl in product(["Family-based", "Family-product-based"],
                                     ["BSN", "Email", "Lift"])}

CONFIGURATIONS = {}
CONFIGURATIONS.update(FEATURE_BASED)
CONFIGURATIONS.update(PRODUCT_BASED)
CONFIGURATIONS.update(FAMILY_BASED)

# These 3 take a long time to run (between 1.5 and 3.5 hours), so it is best
#to run them separately and then merge the results in replay.json.

#CONFIGURATIONS = {
#        ("MinePump", "Family-based"): get_executable("Family-based", "MinePump"),
#        ("MinePump", "Family-product-based"): get_executable("Family-product-based", "MinePump"),
#        ("Cloud", "Product-based"): get_executable("Product-based", "Cloud")
#   }
