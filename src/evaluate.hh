#pragma once

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "rule.h"


typedef struct model {
    rule_t * rules;
    rule_t * labels;

    int ntotal_rules;
    int nlabels;
    int nsamples;
    int nrules;

    unsigned short * ids;
    int * predictions;

    int default_prediction;

    double c;
} model_t;

int model_init_model(model_t * out, const char * model_file, int ntotal_rules, int v);
int model_init(model_t * out, const char * model_file, const char * out_file, const char * label_file, double c, int v);
void model_free(model_t model);


double evaluate(model_t model, int v);
double evaluate(const char * model_file, const char * out_file, const char * label_file, double c, int v);
