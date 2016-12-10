#!/usr/bin/env Rscript
# https://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Classification/JRip
install.packages("caret", dependencies = TRUE, repos="http://cran.rstudio.com/")

library(caret)
library(RWeka)
data(iris)
TrainData <- iris[,1:4]
TrainClasses <- iris[,5]
jripFit <- train(TrainData, TrainClasses,method = "JRip")
