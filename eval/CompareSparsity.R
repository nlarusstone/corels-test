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
if (length(args)  <= 1) {
    stop(sprintf("Usage: CompareSparsity.R [dataset] [outputfile] e.g. CompareSparsity.R compas_0 compas_sparsity.csv\n",
                 args[1]))
}

# 'dataset' used to represent dataset
fname <- args[1]
foutput <- args[2]

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
cartTrainAccs <- c()
cartLeaves <- c()
cps <- c(0.001, 0.003, 0.01, 0.03, 0.1)
## cps <- c(0.001, 0.003, 0.01, 0.03) ## for adult
cartResults <- data.frame(stringsAsFactors=F)

for (val in cps) {
    cartModel <- rpart(Class ~ . , data=as.data.frame(trainData),
                       control = rpart.control(cp=val))

    pred.cartModel <- round(predict(cartModel, newdata=as.data.frame(testDataWOClass)))
    acc <- sum(testData$Class == factor(pred.cartModel[,"X1"], labels=sortednames))/length(testData$Class)
    cartAccs <- c(cartAccs, acc)

    trainPred.cartModel <- round(predict(cartModel, newdata=as.data.frame(trainDataWOClass)))
    tacc <- sum(trainData$Class == factor(trainPred.cartModel[,"X1"], labels=sortednames))/length(trainData$Class)
    cartTrainAccs <- c(cartTrainAccs, tacc)

    leaves <- length(which(cartModel$frame[,"var"]=="<leaf>"))
    cartLeaves <- c(cartLeaves, leaves)
    cartResults <- rbind(cartResults, list(fname, "CART", 0.0, val, 0.0, acc, leaves, tacc))
}
printf("CART:\n")
printf("%s", cat(cps, "\n"))
printf("%s", cat(cartAccs, "\n"))
printf("%s", cat(cartLeaves, "\n"))
printf("%s", cat(cartTrainAccs, "\n"))

## C4.5
## complexity (C) parameters -> 0.05, 0.15, 0.25 (default), 0.35, 0.45
c45Accs <- c()
c45TrainAccs <- c()
c45Leaves <- c()
Cs <- c(0.05, 0.15, 0.25, 0.35, 0.45)
c45Results <- data.frame(stringsAsFactors=F)

for (val in Cs) {
    data_train_fac <- as.data.frame(trainData)
    data_train_fac[,"Class"] <- as.factor(data_train_fac[,"Class"])
    c45Model <- J48(Class ~ ., data=as.data.frame(data_train_fac),
                    control = Weka_control(C=val))

    pred.c45Model <- predict(c45Model, newdata=as.data.frame(testDataWOClass), type="class")
    acc <- sum(testData$Class == pred.c45Model)/length(testData$Class)
    c45Accs <- c(c45Accs, acc)

    trainPred.c45Model <- predict(c45Model, newdata=as.data.frame(trainDataWOClass), type="class")
    tacc <- sum(trainData$Class == trainPred.c45Model)/length(trainData$Class)
    c45TrainAccs <- c(c45TrainAccs, tacc)

    leaves <- c45Model$classifier$measureNumLeaves()
    c45Leaves <- c(c45Leaves, leaves)
    c45Results <- rbind(c45Results, list(fname, "C4.5", val, 0.0, 0.0, acc, leaves, tacc))
}
printf("C4.5:\n")
printf("%s", cat(Cs, "\n"))
printf("%s", cat(c45Accs, "\n"))
printf("%s", cat(c45Leaves, "\n"))
printf("%s", cat(c45TrainAccs, "\n"))

## RIPPER
ripResults <- data.frame(stringsAsFactors=F)
ripModel <- JRip(Class ~ . , data=as.data.frame(trainData))

pred.ripModel <- predict(ripModel, newdata=as.data.frame(testDataWOClass), type="class")
ripAcc <- sum(testData$Class == pred.ripModel)/length(testData$Class)

trainPred.ripModel <- predict(ripModel, newdata=as.data.frame(trainDataWOClass), type="class")
ripTrainAcc <- sum(trainData$Class == trainPred.ripModel)/length(trainData$Class)

ripRuleLen <- length(as.list(ripModel$classifier$getRuleset()))
ripResults <- rbind(ripResults, list(fname, "RIPPER", 0.0, 0.0, 0.0, ripAcc, ripRuleLen, ripTrainAcc))


printf("RIPPER:\n")
printf("%.4f\n", ripAcc)
printf("%d\n", ripRuleLen)
printf("%.4f\n", ripTrainAcc)

## Write out results
colnames(cartResults) <- c("Fold", "Method", "C", "cp", "R", "accuracy", "leaves", "train_accuracy")
colnames(c45Results) <- c("Fold", "Method", "C", "cp", "R", "accuracy", "leaves", "train_accuracy")
colnames(ripResults) <- c("Fold", "Method", "C", "cp", "R", "accuracy", "leaves", "train_accuracy")
isNewFile <- is.na(file.info(foutput)$size) || file.info(foutput)$size == 0
write.table(cartResults, foutput, row.names=F, col.names=isNewFile,
            append=!isNewFile, quote = F, sep=",")
write.table(c45Results, foutput, row.names=F, col.names=F, append=T,
            quote = F, sep=",")
write.table(ripResults, foutput, row.names=F, col.names=F, append=T,
            quote = F, sep=",")

