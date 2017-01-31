# examples

## COMPAS with 10-fold cross-validation

Use `compas/compas-scores-two-years.csv` to produce files in `data/CrossValidation` :

    cd processing/
    python compas.py
    cd ..

Run our branch-and-bound algorithm on a single training fold using something like :

    cd src/
    make clean
    make
    ./bbcache -b -p 1 -r 0.005 -n 6000000 ../data/CrossValidation/compas_0_train.out  ../data/CrossValidation/compas_0_train.label ../data/CrossValidation/compas_0_train.minor

Run our branch-and-bound algorithm on all 10 folds and compute test error for each using something like :

    cd src/
    make clean
    make
    cd ../eval/
    python eval_model.py compas --minor -b -p 1 -r 0.005 -n 6000000 -k 10

As input to `SBRL` use the same training files, e.g.,

    ../data/CrossValidation/compas_0_train.out
    ../data/CrossValidation/compas_0_train.label

and then for evaluating each fold you'll want to use the corresponding test files, e.g.,

    ../data/CrossValidation/compas_0_test.out
    ../data/CrossValidation/compas_0_test.label

As input to other machine learning algorithms use the original features
(note that labels are in the last column) in files of the form :

    ../data/CrossValidation/compas_0_train.csv

and then for evaluating each of these you'll want the corresponding test files, e.g.,

    ../data/CrossValidation/compas_0_test.csv
