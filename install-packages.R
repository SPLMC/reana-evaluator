#!/usr/bin/env Rscript
# first: install dependent packages
install.packages(c("MASS", "akima", "robustbase"))
 
# second: install suggested packages
install.packages(c("cobs", "robust", "mgcv", "scatterplot3d", "quantreg", "rrcov", "lars", "pwr", "trimcluster", "parallel", "mc2d", "psych", "Rfit"))
 
# third: install WRS
install.packages("WRS", repos="http://R-Forge.R-project.org", type="source")

#Optparse package
install.packages("optparse", repos="http://R-Forge.R-project.org")