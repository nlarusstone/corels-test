#!/usr/bin/env Rscript

##
## CompareSparsity.R
##
## Loads a particular dataset via the command line
## and prints sparsity results for the following methods:
## 1) CART (Classification and Regression Trees)
## 2) C4.5
## 3) RIPPER

# increase Java Heap size, e.g., see
# https://stackoverflow.com/questions/21937640/handling-java-lang-outofmemoryerror-when-writing-to-excel-from-r
library(rJava)
options(java.parameters = "-Xmx12000m")

# garbage collection, also from above link
jgc <- function()
{
  .jcall("java/lang/System", method = "gc")
}

printf <- function(...) cat(sprintf(...))

args = commandArgs(TRUE)
if (length(args)  <= 1) {
    stop(sprintf("Usage: CompareSparsity.R [dataset] [outputfile] e.g. CompareSparsity.R compas_0 compas_sparsity.csv\n",
                 args[1]))
}

# 'dataset' used to represent dataset
fname <- args[1]
foutput <- args[2]
fpreds <- args[3]

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

# predictions <- data.frame(stringsAsFactors=F)
nn <- length(testData$Class)
neg <- as.numeric(testData$Class) == 1
pos <- as.numeric(testData$Class) == 2

## CART
## complexity (cp) parameters -> 0.01 (default), 0.003, 0.001, 0.03, 0.1
cartAccs <- c()
cartTrainAccs <- c()
cartLeaves <- c()
if (startsWith(fname, "adult")) {
    cps <- c(0.0005, 0.001, 0.002, 0.01, 0.05) ## (using 0.002 because 0.005 is similar to 0.01)
} else {
    cps <- c(0.001, 0.003, 0.01, 0.03, 0.1)
}
cartResults <- data.frame(stringsAsFactors=F)

for (val in cps) {
    printf("val %1.5f\n", val)
    cartModel <- rpart(Class ~ . , data=as.data.frame(trainData),
                       control = rpart.control(cp=val))

    pred.cartModel <- round(predict(cartModel, newdata=as.data.frame(testDataWOClass)))
    acc <- sum(testData$Class == factor(pred.cartModel[,"X1"], labels=sortednames))/length(testData$Class)
    cartAccs <- c(cartAccs, acc)
    predneg <- as.numeric(factor(pred.cartModel[,"X1"], labels=sortednames)) == 1
    predpos <- as.numeric(factor(pred.cartModel[,"X1"], labels=sortednames)) == 2
    tp <- sum(pos & predpos)
    fp <- sum(neg & predpos)
    fn <- sum(pos & predneg)
    tn <- sum(neg & predneg)
    tpr <- tp / (tp + fn)
    fpr <- fp / (fp + tn)
    printf("%d %d %d %d %d %1.5f %1.5f %1.5f %1.5f\n", nn, tp, fp, fn, tn, tpr, fpr, acc, (tp + tn) / (tp + tn + fp + fn))

    trainPred.cartModel <- round(predict(cartModel, newdata=as.data.frame(trainDataWOClass)))
    tacc <- sum(trainData$Class == factor(trainPred.cartModel[,"X1"], labels=sortednames))/length(trainData$Class)
    cartTrainAccs <- c(cartTrainAccs, tacc)

    leaves <- length(which(cartModel$frame[,"var"]=="<leaf>"))
    cartLeaves <- c(cartLeaves, leaves)
    cartResults <- rbind(cartResults, list(fname, "CART", 0.0, val, 0.0, acc, leaves, tacc, nn, tp, fp, fn, tn, tpr, fpr))
    # predictions <- rbind(predictions, pred.cartModel[,"X1"])
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
if (startsWith(fname, "adult")) {
    Cs <- c(0.00001, 0.0001, 0.001, 0.01, 0.1)
} else if (startsWith(fname, "frisk")) {
    Cs <- c(0.00001, 0.0001, 0.0005, 0.001)
} else if (startsWith(fname, "weapon") || startsWith(fname, "cpw")) {
    Cs <- c(0.00001, 0.0001, 0.001)
} else {
    Cs <- c(0.05, 0.15, 0.25, 0.35, 0.45)
}
c45Results <- data.frame(stringsAsFactors=F)

for (val in Cs) {
    data_train_fac <- as.data.frame(trainData)
    data_train_fac[,"Class"] <- as.factor(data_train_fac[,"Class"])
    c45Model <- J48(Class ~ ., data=as.data.frame(data_train_fac),
                    control = Weka_control(C=val))

    pred.c45Model <- predict(c45Model, newdata=as.data.frame(testDataWOClass), type="class")
    acc <- sum(testData$Class == pred.c45Model)/length(testData$Class)
    c45Accs <- c(c45Accs, acc)
    predneg <- as.numeric(pred.c45Model) == 1
    predpos <- as.numeric(pred.c45Model) == 2
    tp <- sum(pos & predpos)
    fp <- sum(neg & predpos)
    fn <- sum(pos & predneg)
    tn <- sum(neg & predneg)
    tpr <- tp / (tp + fn)
    fpr <- fp / (fp + tn)
    printf("%d %d %d %d %d %1.5f %1.5f %1.5f %1.5f\n", nn, tp, fp, fn, tn, tpr, fpr, acc, (tp + tn) / (tp + tn + fp + fn))

    trainPred.c45Model <- predict(c45Model, newdata=as.data.frame(trainDataWOClass), type="class")
    tacc <- sum(trainData$Class == trainPred.c45Model)/length(trainData$Class)
    c45TrainAccs <- c(c45TrainAccs, tacc)

    leaves <- c45Model$classifier$measureNumLeaves()
    c45Leaves <- c(c45Leaves, leaves)
    c45Results <- rbind(c45Results, list(fname, "C4.5", val, 0.0, 0.0, acc, leaves, tacc, nn, tp, fp, fn, tn, tpr, fpr))
    #predictions <- rbind(predictions, pred.c45Model)
}
printf("C4.5:\n")
printf("%s", cat(Cs, "\n"))
printf("%s", cat(c45Accs, "\n"))
printf("%s", cat(c45Leaves, "\n"))
printf("%s", cat(c45TrainAccs, "\n"))

# garbage collection
gc()
jgc()

## RIPPER
if (!(startsWith(fname, "weapon")) && !(startsWith(fname, "cpw"))) {
    ripResults <- data.frame(stringsAsFactors=F)
    ripModel <- JRip(Class ~ . , data=as.data.frame(trainData))

    pred.ripModel <- predict(ripModel, newdata=as.data.frame(testDataWOClass), type="class")
    ripAcc <- sum(testData$Class == pred.ripModel)/length(testData$Class)
    predneg <- as.numeric(pred.ripModel == 1)
    predpos <- as.numeric(pred.ripModel == 2)
    tp <- sum(pos & predpos)
    fp <- sum(neg & predpos)
    fn <- sum(pos & predneg)
    tn <- sum(neg & predneg)
    tpr <- tp / (tp + fn)
    fpr <- fp / (fp + tn)
    printf("%d %d %d %d %d %1.5f %1.5f %1.5f %1.5f\n", nn, tp, fp, fn, tn, tpr, fpr, acc, (tp + tn) / (tp + tn + fp + fn))

    trainPred.ripModel <- predict(ripModel, newdata=as.data.frame(trainDataWOClass), type="class")
    ripTrainAcc <- sum(trainData$Class == trainPred.ripModel)/length(trainData$Class)

    ripRuleLen <- length(as.list(ripModel$classifier$getRuleset()))
    ripResults <- rbind(ripResults, list(fname, "RIPPER", 0.0, 0.0, 0.0, ripAcc, ripRuleLen, ripTrainAcc, nn, tp, fp, fn, tn, tpr, fpr))
    #predictions <- rbind(predictions, pred.ripModel)

    printf("RIPPER:\n")
    printf("%.4f\n", ripAcc)
    printf("%d\n", ripRuleLen)
    printf("%.4f\n", ripTrainAcc)
}

## Write out results
colnames(cartResults) <- c("Fold", "Method", "C", "cp", "R", "accuracy", "leaves", "train_accuracy", "ntest", "TP", "FP", "FN", "TN", "TPR", "FPR")
colnames(c45Results) <- c("Fold", "Method", "C", "cp", "R", "accuracy", "leaves", "train_accuracy", "ntest", "TP", "FP", "FN", "TN", "TPR", "FPR")
if (!(startsWith(fname, "weapon")) && !(startsWith(fname, "cpw"))) {
    colnames(ripResults) <- c("Fold", "Method", "C", "cp", "R", "accuracy", "leaves", "train_accuracy", "ntest", "TP", "FP", "FN", "TN", "TPR", "FPR")
}
isNewFile <- is.na(file.info(foutput)$size) || file.info(foutput)$size == 0
write.table(cartResults, foutput, row.names=F, col.names=isNewFile,
            append=!isNewFile, quote = F, sep=",")
write.table(c45Results, foutput, row.names=F, col.names=F, append=T,
            quote = F, sep=",")
if (!(startsWith(fname, "weapon")) && !(startsWith(fname, "cpw"))) {
    write.table(ripResults, foutput, row.names=F, col.names=F, append=T,
                quote = F, sep=",")
}
#isNewFile <- is.na(file.info(fpreds)$size) || file.info(fpreds)$size == 0
#write.table(predictions, fpreds, row.names=F, col.names=F, append=T, quote=F, sep=" ")
