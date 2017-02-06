#!/usr/bin/env Rscript

##
## CompareSparsity.R
##
## Loads a particular dataset via the command line
## and prints sparsity results for the following methods:
## 1) CART (Classification and Regression Trees)
## 2) C4.5
## 3) RIPPER


printf <- function(...) cat(sprintf(...))

args = commandArgs(TRUE)
if (length(args)  == 0) {
    stop(sprintf("Usage: CompareSparsity.R [dataset] e.g. CompareSparsity.R compas_0\n",
                 args[1]))
}

# 'dataset' used to represent dataset
fname <- args[1]

printf("Assumes data is in data/CrossValidation\n")
printf("Running %s_{train|test}-binary.csv ", fname)
printf("against CART, C4.5, and RIPPER\n\n")

datadir <- "../data/CrossValidation"
traincsv <- paste(datadir, sprintf("%s_train-binary.csv", fname), sep = "/")
testcsv <- paste(datadir, sprintf("%s_test-binary.csv", fname), sep = "/")

list.of.packages <- c("RWeka", "rpart")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if (length(new.packages) > 0)
    install.packages(new.packages,
                     dependencies = TRUE, repos="http://cran.rstudio.com/")

set.seed(2017)

library(rpart)
library(RWeka)

trainData <- read.csv(traincsv, header = TRUE, sep = ",")
testData <- read.csv(testcsv, header = TRUE, sep = ",")

colnames(trainData)[ncol(trainData)] <- "Class"
colnames(testData)[ncol(trainData)] <- "Class"

sortednames <- sort(make.names(unique(trainData$Class)))
trainData$Class <-factor(trainData$Class, labels=sortednames)
testData$Class <-factor(testData$Class, labels=sortednames)

trainDataWOClass <- subset(trainData, select=-c(Class))
testDataWOClass <- subset(testData, select=-c(Class))


## CART
## complexity (cp) parameters -> 0.01 (default), 0.003, 0.001, 0.03, 0.1
cartAccs <- c()
cartLeaves <- c()
cps <- c(0.001, 0.003, 0.01, 0.03, 0.1)

for (val in cps) {
    cartModel <- rpart(Class ~ . , data=as.data.frame(trainData),
                       control = rpart.control(cp=val))
    pred.cartModel <- round(predict(cartModel, newdata=as.data.frame(testDataWOClass)))
    cartAccs <- c(cartAccs, sum(testData$Class == factor(pred.cartModel[,"X1"], labels=sortednames))/length(testData$Class))
    cartLeaves <- c(cartLeaves, length(which(cartModel$frame[,"var"]=="<leaf>")))
}
printf("CART:\n")
printf("%s", cat(cps, "\n"))
printf("%s", cat(cartAccs, "\n"))
printf("%s", cat(cartLeaves, "\n"))


## C4.5
## complexity (C) parameters -> 0.05, 0.15, 0.25 (default), 0.35, 0.45
c45Accs <- c()
c45Leaves <- c()
Cs <- c(0.05, 0.15, 0.25, 0.35, 0.45)

for (val in Cs) {
    data_train_fac <- as.data.frame(trainData)
    data_train_fac[,"Class"] <- as.factor(data_train_fac[,"Class"])
    c45Model <- J48(Class ~ ., data=as.data.frame(data_train_fac),
                    control = Weka_control(C=val))
    pred.c45Model <- predict(c45Model, newdata=as.data.frame(testDataWOClass), type="class")
    c45Accs <- c(c45Accs, sum(testData$Class == pred.c45Model)/length(testData$Class))
    c45Leaves <- c(c45Leaves, c45Model$classifier$measureNumLeaves())
}
printf("C4.5:\n")
printf("%s", cat(Cs, "\n"))
printf("%s", cat(c45Accs, "\n"))
printf("%s", cat(c45Leaves, "\n"))


## RIPPER
ripModel <- JRip(Class ~ . , data=as.data.frame(trainData))
pred.ripModel <- predict(ripModel, newdata=as.data.frame(testDataWOClass), type="class")
ripAcc <- sum(testData$Class == pred.ripModel)/length(testData$Class)
ripRuleLen <- length(as.list(ripModel$classifier$getRuleset()))
printf("RIPPER:\n")
printf("%.4f\n", ripAcc)
printf("%d\n", ripRuleLen)
