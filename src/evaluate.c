#include "rulelib.h"

/**

    Parameters:
        model - file containing optimal rule list and predictions
        out - .out file containing data
        label - .label file
        c - length constant

    Returns:
        On success:
            (double) objective of rule list evaluated with given data

        On failure:
            -1.0

**/
double evaluate(char * model, char * out, char * label, double c)
{
    int nrules, nsamples, nlabels, nsamples_check;
    rule_t *rules, *labels;

    unsigned short * rulelist_ids;
    int * rulelist_predictions;

    // TODO: load model

    int r = rules_init(out, &nrules, &nsamples, &rules, 1);
    int l = rules_init(label, &nlabels, &nsamples_check, &labels, 0);

    // Sanity check
    if(r != 0) {
        printf("ERROR: Could not read .out file at path '%s'\n", out);
        return -1.0;
    }
    if(l != 0) {
        printf("ERROR: Could not read .label file at path '%s'\n", label);
        return -1.0;
    }

    rulelist_ids = malloc(sizeof(unsigned short) * nrules);
    rulelist_predictions = malloc(sizeof(int) * nrules);

}
