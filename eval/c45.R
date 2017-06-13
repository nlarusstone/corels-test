#!/usr/bin/env Rscript

##
## Compare.R
##
## Loads a particular dataset via the command line
## and runs the following methods:
## 1) GLM (Logistic Regression) -- Generalized Linear Models
## 2) SVM (Support Vector Machines)
## 3) Adaboost
## 4) CART (Classification and Regression Trees)
## 5) C4.5
## 6) RF (Random Forests)
## 7) RIPPER (Repeated Incremental Pruning to Produce Error Reduction)


printf <- function(...) cat(sprintf(...))

args = commandArgs(TRUE)
if (length(args)  == 0) {
    stop(sprintf("Usage: c45.R [dataset] e.g. c45.R compas_0\n",
                 args[1]))
}

# 'dataset' used to represent dataset
fname <- args[1]

printf("Assumes data is in data/CrossValidation\n")
printf("Running %s_{train|test}-binary.csv ", fname)
printf("against GLM, SVM, GBM, CART, C5.0, RF, and RIPPER\n\n");

datadir <- "../data/CrossValidation"
traincsv <- paste(datadir, sprintf("%s_train-binary.csv", fname), sep = "/")
testcsv <- paste(datadir, sprintf("%s_test-binary.csv", fname), sep = "/")

list.of.packages <- c("RWeka", "ggplot2", "gbm", "kernlab", "ada",
                      "svmRadial", "rpart", "randomForest")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if (length(new.packages) > 0)
    install.packages(new.packages,
                     dependencies = TRUE, repos="http://cran.rstudio.com/")

set.seed(2017)

library(kernlab)
library(rpart)
library(ada)
library(RWeka)
library(randomForest)

trainData <- read.csv(traincsv, header = TRUE, sep = ",")
testData <- read.csv(testcsv, header = TRUE, sep = ",")
colnames(trainData)[ncol(trainData)] <- "Class"
colnames(testData)[ncol(trainData)] <- "Class"


sortednames <- sort(make.names(unique(trainData$Class)))
trainData$Class <-factor(trainData$Class, labels=sortednames)
testData$Class <-factor(testData$Class, labels=sortednames)

trainDataWOClass <- subset(trainData, select=-c(Class))
testDataWOClass <- subset(testData, select=-c(Class))

results <- c()

## C4.5
data_train_fac <- as.data.frame(trainData)
data_train_fac[,"Class"] <- as.factor(data_train_fac[,"Class"])
c45_model <- J48(Class ~ ., data=as.data.frame(data_train_fac))
pred.c45Model <- predict(c45_model, newdata=as.data.frame(testDataWOClass), type="class")
c45Acc <- sum(testData$Class == pred.c45Model)/length(testData$Class)
printf("C4.5 result: %.4f\n", c45Acc)
results <- c(results, c45Acc)
