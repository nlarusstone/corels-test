#include "evaluate.hh"

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
double evaluate(char * model, char * out, char * label, double c, int v)
{
    int nrules, nsamples, nlabels, nsamples_check;
    rule_t *rules, *labels;

    unsigned short * rulelist_ids;
    int * rulelist_predictions;

    if(rules_init(out, &nrules, &nsamples, &rules, 1) != 0) {
        if(v > 0)
            printf("ERROR: Could not read .out file at path '%s'\n", out);

        return -1.0;
    }

    if(rules_init(label, &nlabels, &nsamples_check, &labels, 0) != 0) {
        if(v > 0)
            printf("ERROR: Could not read .label file at path '%s'\n", label);

        rules_free(rules, nrules, 1);

        return -1.0;
    }

    // Sanity check
    if(nsamples != nsamples_check) {
        if(v > 0)
            printf("ERROR: nsamples mismatch between .out and .label files\n");

        rules_free(rules, nrules, 1);
        rules_free(labels, nlabels, 0);
    }

    //rulelist_ids = malloc(sizeof(unsigned short) * (nrules - 1));
    //rulelist_predictions = malloc(sizeof(int) * (nrules - 1));

    // Load model

    // default rule
    int default_pred = 1;

    VECTOR total_captured;
    rule_vinit(nsamples, &total_captured);

    int total_ncaptured = 0;
    int total_nincorrect = 0;

    for(int i = 0; i < nrules-1; i++) {
        rule_t rule = rules[rulelist_ids[i]];
        int pred = rulelist_predictions[i];
        int len = i + 1;

        VECTOR captured, captured_correct;
        rule_vinit(nsamples, &captured);
        rule_vinit(nsamples, &captured_correct);

        int ncaptured, ncorrect, temp;

        // Get which ones are captured by the current rule
        rule_vandnot(captured, rule.truthtable, total_captured, nsamples, &ncaptured);
        rule_vor(total_captured, total_captured, captured, nsamples, &temp);

        total_ncaptured += ncaptured;

        rule_vand(captured_correct, captured, labels[pred].truthtable, nsamples, &ncorrect);

        total_nincorrect += (ncaptured - ncorrect);

        if(v > 2) {
            VECTOR default_correct;
            int ndefault_correct;
            rule_vinit(nsamples, &default_correct);

            double lower_bound = (double)total_nincorrect / (double)nsamples + (double)len * c;

            rule_vandnot(default_correct, labels[default_pred].truthtable, total_captured, nsamples, &ndefault_correct);

            double objective = lower_bound + (double)(nsamples - total_ncaptured - ndefault_correct) / (double)nsamples;

            printf("Rule #%d (id: %d, prediction: %s) processed:\n" \
                   "    ncaptured: %d    ncaptured correctly: %d (%.1f)    lower bound: %.6f    objective: %.6f\n",
                   i+1, rulelist_ids[i], pred ? "true" : "false",
                   ncaptured, ncorrect, (double)ncorrect / (double)ncaptured, lower_bound, objective);

            rule_vfree(&default_correct);
        }

        rule_vfree(&captured);
        rule_vfree(&captured_correct);
    }

    VECTOR default_correct;
    int ndefault_correct;

    rule_vinit(nsamples, &default_correct);
    rule_vandnot(default_correct, labels[default_pred].truthtable, total_captured, nsamples, &ndefault_correct);
    rule_vfree(&default_correct);

    total_nincorrect += (nsamples - total_ncaptured - ndefault_correct);

    double objective = (double)total_nincorrect / (double)nsamples + (double)(nrules - 1) * c;

    if(v > 1) {
        double incorrect_frac = (double)total_nincorrect / (double)nsamples;

        printf("\nFinal results:\n" \
               "    objective: %.8f    total captured (excluding default): %d    total incorrect: %d (%.1f)    accuracy: %.1f\n",
               objective, total_ncaptured, total_nincorrect, incorrect_frac, 1.0 - incorrect_frac);
    }

    rules_free(rules, nrules, 1);
    rules_free(labels, nlabels, 0);

    free(rulelist_ids);
    free(rulelist_predictions);

    rule_vfree(&total_captured);

    return objective;
}
