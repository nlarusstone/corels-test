#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "rule.h"


typedef struct model {
    rule_t * rules;
    rule_t * labels;
    rule_t * minority;

    int ntotal_rules;
    int nlabels;
    int nsamples;
    int nrules;
    int nminority;

    unsigned short * ids;
    int * predictions;

    int default_prediction;

    double c;
} model_t;

int model_init_model(model_t * out, const char * model_file, int ntotal_rules, int v);
int model_init(model_t * out, const char * model_file, const char * out_file, const char * label_file, const char * minor_file, double c, int v);
void model_free(model_t model);


double obj_brute(const char * out_file, const char * label_file, double c, int v);
double obj_brute(model_t model, double c, int v);
void _obj_brute_helper(model_t model, int prefix_len, double * min_obj, int v);

double evaluate(model_t model, int v);
double evaluate(const char * model_file, const char * out_file, const char * label_file, double c, int v);
