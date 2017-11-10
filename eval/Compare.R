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

options(warn=1)

# increase Java Heap size, e.g., see
# https://stackoverflow.com/questions/21937640/handling-java-lang-outofmemoryerror-when-writing-to-excel-from-r
library(rJava)
options(java.parameters = "-Xmx12000m")

# garbage collection, also from above link
jgc <- function()
{
  .jcall("java/lang/System", method = "gc")
}

confusionMatrix <- function(pos, neg, predpos, predneg) {
    tp <- sum(pos & predpos)
    fp <- sum(neg & predpos)
    fn <- sum(pos & predneg)
    tn <- sum(neg & predneg)
    tpr <- tp / (tp + fn)
    fpr <- fp / (fp + tn)
    printf("%d %d %d %d %d %1.5f %1.5f %1.5f\n", nn, tp, fp, fn, tn, tpr, fpr, (tp + tn) / (tp + tn + fp + fn))
    list(tp, fp, fn, tn, tpr, fpr)
}

printf <- function(...) cat(sprintf(...))

args = commandArgs(TRUE)
if (length(args)  == 0) {
    stop(sprintf("Usage: Compare.R [dataset] [outfile] e.g. Compare.R compas_0 compas_compare.csv\n"))
}

# 'dataset' used to represent dataset
fname <- args[1]
foutput <- args[2]

printf("Assumes data is in data/CrossValidation\n")
printf("Running %s_{train|test}-binary.csv ", fname)
printf("against GLM, SVM, GBM, CART, C5.0, RF, and RIPPER\n\n");

datadir <- "../data/CrossValidation"
traincsv <- paste(datadir, sprintf("%s_train-binary.csv", fname), sep = "/")
testcsv <- paste(datadir, sprintf("%s_test-binary.csv", fname), sep = "/")

list.of.packages <- c("RWeka", "ggplot2", "gbm", "kernlab", "ada",
                      "rpart", "randomForest")
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

trainData <- read.csv(traincsv, header = TRUE, sep = ",", fileEncoding="UTF-8")
testData <- read.csv(testcsv, header = TRUE, sep = ",")
printf("TRAIN\n")
colnames(trainData)[ncol(trainData)] <- "Class"
printf("TEST ncols: %d cols: \n", ncol(trainData))
printf(colnames(testData))
colnames(testData)[ncol(trainData)] <- "Class"
printf("\nDONE\n")

sortednames <- sort(make.names(unique(trainData$Class)))
trainData$Class <-factor(trainData$Class, labels=sortednames)
testData$Class <-factor(testData$Class, labels=sortednames)

trainDataWOClass <- subset(trainData, select=-c(Class))
testDataWOClass <- subset(testData, select=-c(Class))

nn <- length(testData$Class)
neg <- as.numeric(testData$Class) == 1
pos <- as.numeric(testData$Class) == 2

results <- c()
resultsTable <- data.frame(Fold=character(), Method=character(), C=double(), cp=double(), R=double(), accuracy=double(), leaves=integer(), train_accuracy=double(), ntest=integer(), TP=integer(), FP=integer(), FN=integer(), TN=integer(), TPR=double(), FPR=double(), stringsAsFactors=F)

nrows <- 0

## Logistic Regression
glmModel <- glm(Class ~ . , family=binomial(link="logit"), data=as.data.frame(trainData))
pred.glmModel <- factor(round(predict(glmModel, newdata=as.data.frame(testDataWOClass), type="response")),
                        labels=sortednames)
glmAcc <- sum(testData$Class == pred.glmModel)/length(testData$Class)
printf("GLM accuracy: %.4f\n", glmAcc)
results <- c(results, glmAcc)
predneg <- as.numeric(pred.glmModel) == 1
predpos <- as.numeric(pred.glmModel) == 2
cm <- confusionMatrix(pos, neg, predpos, predneg)
nrows <- nrows + 1
resultsTable[nrows,] <- c(list(fname, "GLM", 0., 0., 0., glmAcc, 0, 0., nn), cm)

## Support Vector Machines
if (!(startsWith(fname, "cpw"))) {
    svmModel <- ksvm(x=as.matrix(trainDataWOClass), y=as.factor(trainData$Class), kernel="rbfdot")
    pred.svmModel <- predict(svmModel, newdata=testDataWOClass, type="response")
    print("%s", cat(testData$Class))
    print("%s", cat(pred.svmModel))
    svmAcc <- sum(testData$Class == pred.svmModel)/length(testData$Class)
    printf("SVM (with RBF kernel) result: %.4f\n", svmAcc)
    results <- c(results, svmAcc)
    predneg <- as.numeric(pred.svmModel) == 1
    predpos <- as.numeric(pred.svmModel) == 2
    cm <- confusionMatrix(pos, neg, predpos, predneg)
    nrows <- nrows + 1
    resultsTable[nrows,] <- c(list(fname, "SVM", 0., 0., 0., svmAcc, 0, 0., nn), cm)
}

## AdaBoost
boostModel <- ada(x = trainDataWOClass, y=trainData$Class)
pred.boostModel <- predict(boostModel, newdata=testDataWOClass)
boostAcc <- sum(testData$Class == pred.boostModel)/length(testData$Class)
printf("AdaBoost result: %.4f\n", boostAcc)
results <- c(results, boostAcc)
predneg <- as.numeric(pred.boostModel) == 1
predpos <- as.numeric(pred.boostModel) == 2
cm <- confusionMatrix(pos, neg, predpos, predneg)
nrows <- nrows + 1
resultsTable[nrows,] <- c(c(fname, "AdaBoost", 0., 0., 0., boostAcc, 0, 0., nn), cm)
warnings()

## CART
cartModel <- rpart(Class ~ . , data=as.data.frame(trainData))
pred.cartModel <- round(predict(cartModel, newdata=as.data.frame(testDataWOClass)))
cartAcc <- sum(testData$Class == factor(pred.cartModel[,"X1"], labels=sortednames))/length(testData$Class)
printf("CART result: %.4f\n", cartAcc)
results <- c(results, cartAcc)
predneg <- as.numeric(factor(pred.cartModel[,"X1"], labels=sortednames)) == 1
predpos <- as.numeric(factor(pred.cartModel[,"X1"], labels=sortednames)) == 2
cm <- confusionMatrix(pos, neg, predpos, predneg)
nrows <- nrows + 1
resultsTable[nrows,] <- c(list(fname, "CART", 0., 0.01, 0., cartAcc, 0, 0., nn), cm)

## C4.5
data_train_fac <- as.data.frame(trainData)
data_train_fac[,"Class"] <- as.factor(data_train_fac[,"Class"])
c45_model <- J48(Class ~ ., data=as.data.frame(data_train_fac))
pred.c45Model <- predict(c45_model, newdata=as.data.frame(testDataWOClass), type="class")
c45Acc <- sum(testData$Class == pred.c45Model)/length(testData$Class)
printf("C4.5 result: %.4f\n", c45Acc)
results <- c(results, c45Acc)
predneg <- as.numeric(pred.c45Model) == 1
predpos <- as.numeric(pred.c45Model) == 2
cm <- confusionMatrix(pos, neg, predpos, predneg)
nrows <- nrows + 1
resultsTable[nrows,] <- c(list(fname, "C4.5", 0.25, 0., 0., c45Acc, 0, 0., nn), cm)


# RandomForests
rfModel <- randomForest(x=trainDataWOClass, y=as.factor(trainData$Class))
pred.rfModel <- predict(rfModel, newdata=as.data.frame(testDataWOClass), type="class")
rfAcc <- sum(testData$Class == pred.rfModel)/length(testData$Class)
printf("Random Forests result: %.4f\n", rfAcc)
results <- c(results, rfAcc)
predneg <- as.numeric(pred.rfModel) == 1
predpos <- as.numeric(pred.rfModel) == 2
cm <- confusionMatrix(pos, neg, predpos, predneg)
nrows <- nrows + 1
resultsTable[nrows,] <- c(list(fname, "RF", 0., 0., 0., rfAcc, 0, 0., nn), cm)

## RIPPER
if (!(startsWith(fname, "weapon")) && !(startsWith(fname, "cpw"))) {
    ripModel <- JRip(Class ~ . , data=as.data.frame(trainData))
    pred.ripModel <- predict(ripModel, newdata=as.data.frame(testDataWOClass), type="class")
    ripAcc <- sum(testData$Class == pred.ripModel)/length(testData$Class)
    printf("RIPPER result: %.4f\n", ripAcc)
    results <- c(results, ripAcc)
    predneg <- as.numeric(pred.ripModel) == 1
    predpos <- as.numeric(pred.ripModel) == 2
    cm <- confusionMatrix(pos, neg, predpos, predneg)
    nrows <- nrows + 1
    resultsTable[nrows,] <- c(list(fname, "RF", 0., 0., 0., ripAcc, 0, 0., nn), cm)
}

printf("%s", cat(results))

## Write out results

isNewFile <- is.na(file.info(foutput)$size) || file.info(foutput)$size == 0
write.table(resultsTable, foutput, row.names=F, col.names=isNewFile,
            append=!isNewFile, quote = F, sep=",")
