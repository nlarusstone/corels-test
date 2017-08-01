#include "evaluate.hh"


int model_init_model(model_t * out, const char * model_file, int ntotal_rules, int v)
{
    FILE * model_p = NULL;
    if((model_p = fopen(model_file, "r")) == NULL) {
        if(v > 0)
            printf("Error opening model file at path '%s'\n", model_file);
        return 1;
    }

    fseek(model_p, 0L, SEEK_END);
    long size = ftell(model_p);
    rewind(model_p);

    char * buffer = (char*)malloc(sizeof(char) * (size + 1));

    long r = fread(buffer, sizeof(char), size, model_p);
    if(r != size) {
        if(v > 0)
            printf("Error reading model file at path '%s'\n", model_file);
        free(buffer);
        fclose(model_p);
        return 1;
    }
    buffer[size] = '\0';

    fclose(model_p);

    char * prev_rule_loc = buffer - 1;
    char * rule_loc = NULL;
    int nrules = 0;
    int default_pred = 0;

    out->ids = (unsigned short*)malloc(sizeof(unsigned short));
    out->predictions = (int*)malloc(sizeof(int));

    while((rule_loc = strchr(prev_rule_loc + 1, '~')) != NULL) {

        char * feature_start = prev_rule_loc + 3;
        if(prev_rule_loc == (buffer - 1))
            feature_start = buffer;

        int feature_len = (rule_loc - feature_start);

        if(strncmp("default", feature_start, feature_len) == 0) {
            default_pred = *(rule_loc + 1) - '0';
            break;
        }
        else {
            int found = 0;

            for(int i = 1; i < ntotal_rules; i++) {
                if(strncmp(out->rules[i].features, feature_start, feature_len) == 0) {
                    if(++nrules >= ntotal_rules) {
                        if(v > 0)
                            printf("Error: rule number overflow\n");
                        free(out->ids);
                        out->ids = NULL;
                        free(out->predictions);
                        out->predictions = NULL;
                        free(buffer);
                        return 1;
                    }

                    found = 1;

                    out->ids = (unsigned short*)realloc(out->ids, nrules);
                    out->predictions = (int*)realloc(out->predictions, nrules);

                    out->ids[nrules-1] = i;
                    out->predictions[nrules-1] = *(rule_loc + 1) - '0';

                    break;
                }
            }

            if(!found) {
                if(v > 0)
                    printf("Error: could not find rule with features '%.*s'\n", feature_len, feature_start);
                free(out->ids);
                out->ids = NULL;
                free(out->predictions);
                out->predictions = NULL;
                free(buffer);
                return 1;
            }
        }

        prev_rule_loc = rule_loc;
    }

    free(buffer);

    out->nrules = nrules;
    out->default_prediction = default_pred;

    return 0;
}

int model_init(model_t * out, const char * model_file, const char * out_file, const char * label_file, double c, int v)
{
    if(rules_init(out_file, &out->ntotal_rules, &out->nsamples, &out->rules, 1) != 0) {
        if(v > 0)
            printf("Error reading .out file at path '%s'\n", out_file);
        return 1;
    }

    int nsamples_check;
    if(rules_init(label_file, &out->nlabels, &nsamples_check, &out->labels, 0) != 0) {
        if(v > 0)
            printf("Error reading .label file at path '%s'\n", label_file);
        rules_free(out->rules, out->ntotal_rules, 1);
        return 1;
    }

    if(out->nsamples != nsamples_check) {
        if(v > 0)
            printf("Error: Nsamples mismatch between .out and .label files\n");

        return 1;
    }

    if(model_init_model(out, model_file, out->ntotal_rules, v) != 0)
        return 1;

    out->c = c;

    return 0;
}

void model_free(model_t model)
{
    if(model.ids)
        free(model.ids);

    if(model.predictions)
        free(model.predictions);

    if(model.rules)
        rules_free(model.rules, model.ntotal_rules, 1);

    if(model.labels)
        rules_free(model.labels, model.nlabels, 0);
}


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
double evaluate(const char * model_file, const char * out_file, const char * label_file, double c, int v)
{
    model_t model;

    if(model_init(&model, model_file, out_file, label_file, c, v) != 0) {
        printf("Error loading model, exiting\n");
        return -1.0;
    }

    double r = evaluate(model, v);

    model_free(model);

    return r;
}

double evaluate(model_t model, int v)
{
    VECTOR total_captured;
    rule_vinit(model.nsamples, &total_captured);

    int total_ncaptured = 0;
    int total_nincorrect = 0;

    // model.nrules doesn't include the default rule
    for(int i = 0; i < model.nrules; i++) {
        rule_t rule = model.rules[model.ids[i]];
        int pred = model.predictions[i];
        int len = i + 1;

        VECTOR captured, captured_correct;
        rule_vinit(model.nsamples, &captured);
        rule_vinit(model.nsamples, &captured_correct);

        int ncaptured, ncorrect, temp;

        // Get which ones are captured by the current rule
        rule_vandnot(captured, rule.truthtable, total_captured, model.nsamples, &ncaptured);
        rule_vor(total_captured, total_captured, captured, model.nsamples, &temp);

        total_ncaptured += ncaptured;

        rule_vand(captured_correct, captured, model.labels[pred].truthtable, model.nsamples, &ncorrect);

        total_nincorrect += (ncaptured - ncorrect);

        if(v > 2) {
            VECTOR default_correct;
            int ndefault_correct;
            rule_vinit(model.nsamples, &default_correct);

            double lower_bound = (double)total_nincorrect / (double)model.nsamples + (double)len * model.c;

            rule_vandnot(default_correct, model.labels[model.default_prediction].truthtable, total_captured, model.nsamples, &ndefault_correct);

            double objective = lower_bound + (double)(model.nsamples - total_ncaptured - ndefault_correct) / (double)model.nsamples;

            printf("Rule #%d (id: %d, prediction: %s) processed:\n" \
                   "    ncaptured: %d    ncaptured correctly: %d (%.1f%%)    lower bound: %.6f    objective: %.6f\n",
                   i+1, model.ids[i], pred ? "true" : "false",
                   ncaptured, ncorrect, 100.0 * (double)ncorrect / (double)ncaptured, lower_bound, objective);

            rule_vfree(&default_correct);
        }

        rule_vfree(&captured);
        rule_vfree(&captured_correct);
    }

    VECTOR default_correct;
    int ndefault_correct;

    rule_vinit(model.nsamples, &default_correct);
    rule_vandnot(default_correct, model.labels[model.default_prediction].truthtable, total_captured, model.nsamples, &ndefault_correct);
    rule_vfree(&default_correct);

    total_nincorrect += (model.nsamples - total_ncaptured - ndefault_correct);

    double incorrect_frac = (double)total_nincorrect / (double)model.nsamples;

    double objective = incorrect_frac + (double)model.nrules * model.c;

    if(v > 1) {
        printf("\nFinal results:\n" \
               "    objective: %.10f    total captured (excluding default): %d    total incorrect: %d (%.3f%%)    accuracy: %.3f%%\n",
               objective, total_ncaptured, total_nincorrect, 100.0 * incorrect_frac, 100.0 - 100.0 * incorrect_frac);
    }

    return objective;
}
