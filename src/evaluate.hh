#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "queue.hh"
#include "evaluate.hh"

#include "rule.h"



/**
    A model is simply a struct to store the roptimal ule list that is outputted by CORELS so it can be tested
**/
typedef struct model {
    rule_t * rules; // All rules
    rule_t * labels; // All labels
    rule_t * minority; // All minority data (mostly redundant)

    int ntotal_rules;
    int nlabels;
    int nsamples;
    int nrules; // Number of rules in the optimal list
    int nminority;

    unsigned short * ids; // ids of the optimal rule list
    int * predictions; // predictions of the optimal rule list

    int default_prediction;

    double c;
} model_t;

int run_random_tests(size_t num_iters, int num_rules, int num_samples, double c, int b_max_list_len,
                     int ablation, std::function<bool(Node*, Node*)> q_cmp, bool useCapturedPMap,
                     size_t max_num_nodes, double epsilon, unsigned long seed, int v);

int output_error(model_t model, tracking_vector<unsigned short, DataStruct::Tree> corels_opt_list,
                 tracking_vector<bool, DataStruct::Tree> corels_opt_preds,
                 tracking_vector<unsigned short, DataStruct::Tree> brute_opt_list,
                 tracking_vector<bool, DataStruct::Tree> brute_opt_preds, double corels_obj,
                 double eval_check_obj, double brute_obj, int v);

/**
    Verbosity usage is common, so explained here:

        value               behavior

        >0              Only fatal errors

        >1              Only most important data
                        (usually, the final results of the function)

        >2              Diverse progress data

**/

// These functions randomize the truthtable of a rule, and for the non-GMP function to work correctly the number of rules
// must be a multiple of BITS_PER_ENTRY (currently, it actually doesn't work, so only use GMP for now)

#ifdef GMP

void
randomize_rule(rule_t * rule, int nsamples, gmp_randstate_t state);

#else

void
randomize_rule(rule_t * rule, int nsamples);

#endif

/**
    Loads the data from a model, out, label, and minor file into a model struct

    Parameters:
        out - pointer to struct in which to store info from files
        model_file - file containing optimal rule list and predictions
        out_file - .out file containing data
        label_file - .label file
        minor_file - .minor file
        c - length constant
        v - verbosity

    Returns:
        On success:
            0

        On failure:
            1
**/
int
model_init(model_t * out, const char * model_file, const char * out_file, const char * label_file, const char * minor_file, double c, int v);



/**
    Called in model_init, loads the ids, predictions, nrules, and default prediction information
    of an optimal rule list stored in model_file

    Parameters:
        out - pointer to struct in which to store info from files
        model_file - file containing optimal rule list and predictions
        ntotal_rules - total number of rules
        v - verbosity

    Returns:
        On success:
            0

        On failure:
            1
**/
int
model_init_model(model_t * out, const char * model_file, int ntotal_rules, int v);



// Frees allocated memory
void model_free(model_t model);




/**
    Calculates the optimal objective from given data by checking every possible rule list and prediction permutation
    Then, it stores the information of the optimal rule list in model

    Parameters:
        model - contains info about the rule data and is where the optimal rule list is stored
        max_list_len - Max length of rule lists checked
        v - verbosity

    Returns:
        On success:
            (double) minimum objective for all the data

        On failure:
            -1.0
**/
double
obj_brute(model_t * model, int max_list_len, int v);



/**
    Recursive helper function for finding all the possible rule lists
**/
void
_obj_brute_helper(model_t model, int prefix_len, double * min_obj, unsigned short * opt_ids,
                  int * opt_predictions, int * opt_default_prediction, int * opt_nrules, int max_list_len, int v);




/**

    Parameters:
        model_file - file containing optimal rule list and predictions
        out_file - .out file containing data
        label_file - .label file
        c - length constant
        v - verbosity

    Returns:
        On success:
            (double) objective of rule list evaluated with given data

        On failure:
            -1.0
**/
double
evaluate(const char * model_file, const char * out_file, const char * label_file, double c, int v);




/**
        Same as before, except it takes a model_t object preloaded
**/
double
evaluate(model_t model, int v);
