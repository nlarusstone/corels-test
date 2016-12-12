#!/usr/bin/env Rscript

## https://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Classification/JRip

## Implements a propositional rule learner:
##  Repeated Incremental Pruning to Produce Error Reduction (RIPPER), which was
##  proposed by William W. Cohen as an optimized version of IREP.
##  It is based in association rules with reduced error pruning (REP),
##  a very common and effective technique found in decision tree algorithms.

list.of.packages <- c("caret", "RWeka")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages) > 0)
    install.packages(new.packages,
                     dependencies = TRUE, repos="http://cran.rstudio.com/")

library(caret)
library(RWeka)
data(iris)
TrainData <- iris[,1:4]
TrainClasses <- iris[,5]
jripFit <- train(TrainData, TrainClasses, method = "JRip")
jripFit
