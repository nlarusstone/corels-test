#!/usr/bin/env Rscript

##
## Compare.R
##
## Loads a particular dataset via the command line
## and runs the following methods:
## 1) GLM (Logistic Regression) -- Generalized Linear Models
## 2) SVM (Support Vector Machines)
## 3) GBM (Boosted Trees) -- Generalized Boosted Models
## 4) CART (Classification and Regression Trees)
## 5) C5.0
## 6) RF (Random Forests)
## 7) RIPPER (Repeated Incremental Pruning to Produce Error Reduction)
## 8) SBRL (Scalable Bayesian Rule Lists)
## Code for 1-6 based on "ExperimentalCode" folder sent to us by Cynthia

#args = commandArgs()
#if (length(args)  <= 1) {
#    stop(sprintf("Usage: %s [dataset path]", args[1]))
#}
#df <- read.csv(args[2], header = TRUE)

list.of.packages <- c("caret", "RWeka", "AER", "pROC",
                      "ggplot2", "gbm", "C50", "repeatedcv",
                      "svmRadial", "rpart", "randomForest",
                      "RColorBrewer", "party", "partykit", "rpart.plot",
                      "sbrl")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if (length(new.packages) > 0)
    install.packages(new.packages,
                     dependencies = TRUE, repos="http://cran.rstudio.com/")

set.seed(2017)

library(AER)
library(caret)
library(pROC)
library(ggplot2)
library(rpart.plot)
library(RColorBrewer)
library(party)
library(partykit)
library(sbrl)

data(tictactoe)

for (name in names(tictactoe)) {
    column <- tictactoe[,name]
    colnames <- make.names(unique(column))
    tictactoe[name] <- factor(column, labels=colnames)
}

tictactoe$Class <- tictactoe$label
sorted_names <- sort(make.names(factor(tictactoe$Class)))
neglabel <- sorted_names[1]
poslabel <- sorted_names[2]
tictactoe <- subset(tictactoe, select=-c(label))

# 9/10 of data for training, 1/10 of data for evaluation/testing
training <- createDataPartition(tictactoe$Class, p = 0.9, list=FALSE)
trainData <- tictactoe[training,]
testData <- tictactoe[-training,]

fitControl <- trainControl(method = "repeatedcv",
                           number = 10,
                           repeats = 5,
                           classProbs = TRUE,
                           summaryFunction = twoClassSummary)

## Logistic Regression
glmModel <- glm(Class ~ . , data=trainData, family=binomial)
pred.glmModel <- predict(glmModel, newdata=testData, type="response")
# Calculate the AUC for the test data set.
roc.glmModel <- pROC::roc(testData$Class, pred.glmModel)
auc.glmModel <- pROC::auc(roc.glmModel)

## Support Vector Machines:
svmModel <- train(Class ~ ., data=trainData, method = "svmRadial", metric="ROC", trControl = fitControl, verbose=FALSE, tuneLength=5)
pred.svmModel <- as.vector(predict(svmModel, newdata=testData, type="prob")[,poslabel])
# Calculate the AUC for the test data set.
roc.svmModel <- pROC::roc(testData$Class, pred.svmModel)
auc.svmModel <- pROC::auc(roc.svmModel)

## Boosted Trees
gbmModel <- train(Class ~ ., data=trainData, method = "gbm", metric="ROC", trControl = fitControl, verbose=FALSE, tuneLength=5)
pred.gbmModel <- as.vector(predict(gbmModel, newdata=testData, type="prob")[,poslabel])
# Calculate the AUC for the test data set.
roc.gbmModel <- pROC::roc(testData$Class, pred.gbmModel)
auc.gbmModel <- pROC::auc(roc.gbmModel)

## CART
cartModel <- train(Class ~ ., data=trainData, method = "rpart", metric="ROC", trControl = fitControl, tuneLength=5)
pred.cartModel <- as.vector(predict(cartModel, newdata=testData, type="prob")[,poslabel])
# Calculate the AUC for the test data set.
roc.cartModel <- pROC::roc(testData$Class, pred.cartModel)
auc.cartModel <- pROC::auc(roc.cartModel)

## C5.0
c50Model <- train(Class ~ ., data=trainData, method = "C5.0", metric="ROC", trControl = fitControl, tuneLength=5)
pred.c50Model <- as.vector(predict(c50Model, newdata=testData, type="prob")[,poslabel])
# Calculate the AUC for the test data set.
roc.c50Model <- pROC::roc(testData$Class, pred.c50Model)
auc.c50Model <- pROC::auc(roc.c50Model)

## Random Forest
rfModel <- train(Class ~ ., data=trainData, method = "rf", metric="ROC", trControl = fitControl, verbose=FALSE, tuneLength=5)
pred.rfModel <- as.vector(predict(rfModel, newdata=testData, type="prob")[,poslabel])
# Calculate the AUC for the test data set.
roc.rfModel <- pROC::roc(testData$Class, pred.rfModel)
auc.rfModel <- pROC::auc(roc.rfModel)

## RIPPER
ripModel <- train(Class ~ ., data=trainData, method = "JRip", metric="ROC", trControl = fitControl, tuneLength=5)
pred.ripModel <- as.vector(predict(ripModel, newdata=testData, type="prob")[,poslabel])
# Calculate the AUC for the test data set.
roc.ripModel <- pROC::roc(testData$Class, pred.ripModel)
auc.ripModel <- pROC::auc(roc.ripModel)

## sbrl
trainData$label <- trainData$Class
sbrlModel <- sbrl(trainData, pos_sign=poslabel, neg_sign=neglabel)
temp <- predict(sbrlModel, testData, type="prob")
# sbrl has $V2 for pos label
pred.sbrlModel <- as.vector(temp$V2)
# Calculate the AUC for the test data set.
roc.sbrlModel <- pROC::roc(testData$Class, pred.sbrlModel)
auc.sbrlModel <- pROC::auc(roc.sbrlModel)

## Plot AUC, on the test data set, for each model.
test.auc <- data.frame(model=c("glm", "svm", "gbm", "cart", "c50", "rForest", "RIPPER", "sbrl"),auc=c(auc.glmModel, auc.svmModel, auc.gbmModel, auc.cartModel, auc.c50Model, auc.rfModel, auc.ripModel, auc.sbrlModel))
test.auc <- test.auc[order(test.auc$auc, decreasing=TRUE),]
test.auc$model <- factor(test.auc$model, levels=test.auc$model)
test.auc

theme_set(theme_gray(base_size = 18))
ggplot(x=model, y=auc, stat="identity", data=test.auc, geom="bar", position = "dodge") +
geom_bar(aes(x=model, y=auc), stat="identity", fill = "light blue")

## Plot tuning parameters that were chosen by repeated CV.
# Logistic Regression
plot(roc.glmModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.40, print.auc.col="blue", type="l", col='blue', lwd=1, lty=1)
# SVM
plot(roc.svmModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.35, print.auc.col="purple", type="l", add=TRUE, col='purple', lwd=1, lty=1)
# Boosted Trees
plot(roc.gbmModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.30, print.auc.col="red", type="l", add=TRUE, col='red', lwd=1, lty=1)
# CART
plot(roc.cartModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.25, print.auc.col="green", type="l", add=TRUE, col='green', lwd=1, lty=1)
# C50
plot(roc.c50Model, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.20, print.auc.col="navy", type="l", add=TRUE, col='navy', lwd=1, lty=1)
# Random Forest
plot(roc.rfModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.15, print.auc.col="yellow", type="l", add=TRUE, col='yellow', lwd=1, lty=1)
# RIPPER
plot(roc.ripModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.10, print.auc.col="orange", type="l", add=TRUE, col='orange', lwd=1, lty=1)
# SBRL
plot(roc.sbrlModel, print.auc=TRUE, print.auc.x=0.7, print.auc.y=0.05, print.auc.col="pink", type="l", add=TRUE, col='pink', lwd=1, lty=1)

legend("bottomright",
       legend=c("logistic regression", "SVM", "Boosted Trees", "CART", "C50", "rForest", "RIPPER", "sbrl"),
       col=c("blue", "purple", "red", "green", "navy","yellow", "orange", "pink"), lwd=1)
