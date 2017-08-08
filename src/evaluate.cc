#include "evaluate.hh"

#ifdef GMP

void randomize_data(data_t data, gmp_randstate_t state)
{
    for(int i = 1; i < data.nrules; i++) {
        randomize_rule(data.rules + i, data.nsamples, state);
    }

    for(int i = 0; i < 2; i++) {
        randomize_rule(data.labels + i, data.nsamples, state);
    }
}

void randomize_rule(rule_t * rule, int nsamples, gmp_randstate_t state)
{
    mpz_rrandomb(rule->truthtable, state, nsamples);
    rule->support = mpz_popcount(rule->truthtable);
}

#else

void randomize_data(data_t data)
{
    for(int i = 1; i < data.nrules; i++) {
        randomize_rule(data.rules + i, data.nsamples);
    }

    for(int i = 0; i < 2; i++) {
        randomize_rule(data.labels + i, data.nsamples);
    }
}

void randomize_rule(rule_t * rule, int nsamples)
{
    int nentries = (nsamples + BITS_PER_ENTRY - 1)/BITS_PER_ENTRY;

    int count = 0;
    for(int i = 0; i < nentries; i++) {
        rule->truthtable[i] = (double)(~(v_entry)0) * (double)rand() / (double)RAND_MAX;
        count += count_ones(rule->truthtable[i]);
    }

    rule->support = count;
}

#endif

double obj_brute(data_t data, rulelist_t * opt_list, int max_list_len, int v)
{
    double min_obj = 1.0;

    rulelist_t temp_list;
    // Temp info, used when calculating each rule list
    temp_list.ids = (unsigned short*)malloc(sizeof(unsigned short) * (data.nrules - 1));
    temp_list.predictions = (int*)malloc(sizeof(int) * (data.nrules - 1));
    temp_list.nrules = 0;

    if(opt_list) {
        opt_list->ids = (unsigned short*)malloc(sizeof(unsigned short) * (data.nrules - 1));
        opt_list->predictions = (int*)malloc(sizeof(int) * (data.nrules - 1));
        opt_list->default_prediction = 0;
        opt_list->nrules = 0;
    }

    max_list_len = max_list_len > data.nrules-1 ? data.nrules-1 : max_list_len;

    for(int i = 0; i < 2; i++) {
        temp_list.default_prediction = i;

        temp_list.nrules = 0;
        double obj = evaluate(data, temp_list, v ? 1 : 0);

        if(obj == -1.0)
            continue;

        if(obj < min_obj) {
            if(v > 2)
                printf("[obj_brute] min obj:  %f -> %f\n", min_obj, obj);

            if(opt_list) {
                opt_list->nrules = 0;
                opt_list->default_prediction = temp_list.default_prediction;
            }
            min_obj = obj;
        }

        if(max_list_len)
            _obj_brute_helper(data, &min_obj, opt_list, temp_list, max_list_len, v);
    }

    if(v > 1) {
        printf("[obj_brute]: Optimal objective: %f\n", min_obj);
    }

    free(temp_list.ids);
    free(temp_list.predictions);

    return min_obj;
}

void _obj_brute_helper(data_t data, double * min_obj, rulelist_t * opt_list, rulelist_t prefix, int max_list_len, int v) {
    for(int rule_id = 1; rule_id < data.nrules; rule_id++) {
        int found = 0;

        for(int i = 0; i < prefix.nrules; i++) {
            if(prefix.ids[i] == rule_id) {
                found = 1;
                break;
            }
        }

        if(found)
            continue;

        for(int label = 0; label < 2; label++) {
            prefix.ids[prefix.nrules] = rule_id;
            prefix.predictions[prefix.nrules] = label;
            prefix.nrules = prefix.nrules + 1;

            double obj = evaluate(data, prefix, v ? 1 : 0);

            if(obj == -1.0) {
                if(v > 0)
                    printf("[obj_brute_helper] Error evaluating a rule list!\n");
                return;
            }

            if(obj < *min_obj) {
                if(v > 2)
                    printf("[obj_brute_helper] min obj:  %f -> %f\n", *min_obj, obj);

                if(opt_list) {
                    memcpy(opt_list->ids, prefix.ids, sizeof(unsigned short) * prefix.nrules);
                    memcpy(opt_list->predictions, prefix.predictions, sizeof(int) * prefix.nrules);
                    *opt_list->default_prediction = prefix.default_prediction;
                    *opt_list->nrules = prefix.nrules;
                }
                *min_obj = obj;
            }

            if(prefix_len < max_list_len-1)
                _obj_brute_helper(data, min_obj, opt_list, prefix, max_list_len, v);
        }
    }
}

int model_init_model(model_t * out, const char * model_file, int ntotal_rules, int v)
{
    FILE * model_p = NULL;
    if((model_p = fopen(model_file, "r")) == NULL) {
        if(v > 0)
            printf("[model_init_model] Error opening model file at path '%s'\n", model_file);
        return 1;
    }

    fseek(model_p, 0L, SEEK_END);
    long size = ftell(model_p);
    rewind(model_p);

    char * buffer = (char*)malloc(sizeof(char) * (size + 1));

    long r = fread(buffer, sizeof(char), size, model_p);
    if(r != size) {
        if(v > 0)
            printf("[model_init_model] Error reading model file at path '%s'\n", model_file);
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
                            printf("[model_init_model] Error: rule number overflow\n");
                        free(out->ids);
                        out->ids = NULL;
                        free(out->predictions);
                        out->predictions = NULL;
                        free(buffer);
                        return 1;
                    }

                    found = 1;

                    out->ids = (unsigned short*)realloc(out->ids, sizeof(unsigned short) * nrules);
                    out->predictions = (int*)realloc(out->predictions, sizeof(int) * nrules);

                    out->ids[nrules-1] = i;
                    out->predictions[nrules-1] = *(rule_loc + 1) - '0';

                    break;
                }
            }

            if(!found) {
                if(v > 0)
                    printf("[model_init_model] Error: could not find rule with features '%.*s'\n", feature_len, feature_start);
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

int model_init(model_t * out, const char * model_file, const char * out_file, const char * label_file, const char * minor_file, double c, int v)
{
    if(rules_init(out_file, &out->ntotal_rules, &out->nsamples, &out->rules, 1) != 0) {
        if(v > 0)
            printf("[model_init] Error reading .out file at path '%s'\n", out_file);
        return 1;
    }

    int nsamples_chk;
    if(rules_init(label_file, &out->nlabels, &nsamples_chk, &out->labels, 0) != 0) {
        if(v > 0)
            printf("[model_init] Error reading .label file at path '%s'\n", label_file);
        rules_free(out->rules, out->ntotal_rules, 1);
        return 1;
    }

    if(out->nsamples != nsamples_chk) {
        if(v > 0)
            printf("[model_init] Error: Nsamples mismatch between .out and .label files\n");

        return 1;
    }

    if(minor_file != NULL) {
        int nsamples_check;
        if(rules_init(minor_file, &out->nminority, &nsamples_check, &out->minority, 0) != 0) {
            if(v > 0)
                printf("model_init] Error reading .minor file at path '%s'\n", minor_file);
            rules_free(out->rules, out->ntotal_rules, 1);
            rules_free(out->labels, out->nlabels, 0);
            return 1;
        }

        if(out->nsamples != nsamples_check) {
            if(v > 0)
                printf("[model_init] Error: Nsamples mismatch between .out and .minor files\n");

            return 1;
        }
    }
    else {
        out->minority = NULL;
        out->nminority = 0;
    }

    if(model_file != NULL) {
        if(model_init_model(out, model_file, out->ntotal_rules, v) != 0)
            return 1;
    }
    else {
        out->ids = NULL;
        out->predictions = NULL;
        out->default_prediction = 0;
    }

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

    if(model.minority)
        rules_free(model.minority, model.nminority, 0);
}


double evaluate(const char * model_file, const char * out_file, const char * label_file, double c, int v)
{
    model_t model;

    if(model_init(&model, model_file, out_file, label_file, NULL, c, v) != 0) {
        printf("[evaluate] Error loading model, exiting\n");
        return -1.0;
    }

    double r = evaluate(model, v);

    model_free(model);

    return r;
}

double evaluate(model_t model, int v)
{
    //printf("%d\n", model.nrules);

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

            printf("[evaluate] Rule #%d (id: %d, prediction: %s) processed:\n" \
                   "[evaluate]     ncaptured: %d    ncaptured correctly: %d (%.1f%%)    lower bound: %.6f    objective: %.6f\n\n",
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
        int ndefault_captured = model.nsamples - total_ncaptured;
        printf("[evaluate] Default rule (prediction: %s) processed:\n" \
               "[evaluate]     ncaptured: %d    ncaptured correctly: %d (%.1f%%)\n\n",
               model.default_prediction ? "true" : "false",
               ndefault_captured, ndefault_correct, 100.0 * (double)ndefault_correct / (double)ndefault_captured);

        printf("\n[evaluate] Final results:\n" \
               "[evaluate]     objective: %.10f    nsamples: %d    total captured (excluding default): %d    total incorrect: %d (%.3f%%)    accuracy: %.3f%%\n",
               objective, model.nsamples, total_ncaptured, total_nincorrect, 100.0 * incorrect_frac, 100.0 - 100.0 * incorrect_frac);
    }

    return objective;
}

int output_error(model_t model, tracking_vector<unsigned short, DataStruct::Tree> corels_opt_list,
                  tracking_vector<bool, DataStruct::Tree> corels_opt_preds,
                  tracking_vector<unsigned short, DataStruct::Tree> brute_opt_list,
                  tracking_vector<bool, DataStruct::Tree> brute_opt_preds, double corels_obj,
                  double eval_check_obj, double brute_obj, int v)
{
    printf("\n\n\n\n/***************************************************************/\n\n");
    printf("Errors were detected in the following set of data:\n\n");

    printf("Dumping rule data:\n");
    for(int i = 0; i < model.ntotal_rules; i++) {
        rule_print(model.rules, i, model.nsamples, 1);
    }

    printf("\nDumping label data:\n");
    for(int i = 0; i < model.nlabels; i++) {
        rule_print(model.labels, i, model.nsamples, 1);
    }

    printf("\n\nOptimal rule list determined by CORELS:\n");
    print_final_rulelist(corels_opt_list, corels_opt_preds, NULL, model.rules, model.labels, NULL);

    if(brute_opt_preds.size()) {
        printf("\nOptimal rule list determined by brute force:\n");
        print_final_rulelist(brute_opt_list, brute_opt_preds, NULL, model.rules, model.labels, NULL);

        printf("\nOptimal objective determined by CORELS: %f\n" \
               "Objective of optimal rule list determined by CORELS: %f\n" \
               "Optimal objective determined by brute-force: %f\n\n",
               corels_obj, eval_check_obj, brute_obj);
    }
    else {
        printf("\nOptimal objective determined by CORELS: %f\n" \
               "Objective of optimal rule list determined by CORELS: %f\n\n",
               corels_obj, eval_check_obj);
    }

    return 0;
}

int run_random_tests(size_t num_iters, int num_rules, int num_samples, double c, int b_max_list_len,
                     int ablation, std::function<bool(Node*, Node*)> q_cmp, bool useCapturedPMap,
                     size_t max_num_nodes, double epsilon, unsigned long seed, int v)
{
    model_t model;

    model.ntotal_rules = num_rules;
    model.nlabels = 2;
    model.nsamples = num_samples;
    model.c = c;

    model.nrules = 0;
    model.default_prediction = 0;
    model.ids = NULL;
    model.predictions = NULL;
    model.minority = NULL;
    model.nminority = 0;
    model.rules = (rule_t*)malloc(sizeof(rule_t) * model.ntotal_rules);
    model.labels = (rule_t*)malloc(sizeof(rule_t) * model.nlabels);

    for(int i = 1; i < model.ntotal_rules; i++) {
        rule_vinit(model.nsamples, &model.rules[i].truthtable);
        model.rules[i].support = 0;
        model.rules[i].cardinality = 1;

        char number[64];
        sprintf(number, "%d", i);

        int numlen = strlen(number);
        model.rules[i].features = (char*)malloc(sizeof(char) * (numlen + 7));

        strcpy(model.rules[i].features, "{rule");
        strcat(model.rules[i].features, number);
        strcat(model.rules[i].features, "}");
    }

    // Default rule
    rule_vinit(model.nsamples, &model.rules[0].truthtable);
    make_default(&model.rules[0].truthtable, model.nsamples);

    model.rules[0].support = model.nsamples;
    model.rules[0].cardinality = 1;

    model.rules[0].features = (char*)malloc(sizeof(char) * 8);
    strcpy(model.rules[0].features, "default");


    for(int i = 0; i < model.nlabels; i++) {
        rule_vinit(model.nsamples, &model.labels[i].truthtable);
        model.labels[i].support = 0;
        model.labels[i].cardinality = 1;

        char number[64];
        sprintf(number, "%d", i);

        int numlen = strlen(number);
        model.labels[i].features = (char*)malloc(sizeof(char) * (numlen + 9));

        strcpy(model.labels[i].features, "{label=");
        strcat(model.labels[i].features, number);
        strcat(model.labels[i].features, "}");
    }

    int returnCode = 0;

#ifdef GMP
    gmp_randstate_t rand_state;

    gmp_randinit_mt(rand_state);

    gmp_randseed_ui(rand_state, seed);
#else
    srand(seed);
#endif

    bool exit = false;
    for(size_t i = 0; i < num_iters && !exit; i++)
    {
        for(int i = 1; i < model.ntotal_rules; i++) {
#ifdef GMP
            randomize_rule(&model.rules[i], model.nsamples, rand_state);
#else
            randomize_rule(&model.rules[i], model.nsamples);
#endif
        }

#ifdef GMP
        randomize_rule(&model.labels[0], model.nsamples, rand_state);
#else
        randomize_rule(&model.labels[0], model.nsamples);
#endif

        int temp = 0;
        rule_not(model.labels[1].truthtable, model.labels[0].truthtable, model.nsamples, &temp);

#ifdef GMP
        VECTOR tmp;
        rule_vinit(model.nsamples, &tmp);
        mpz_ui_pow_ui(tmp, 2, model.nsamples);
        mpz_sub_ui(tmp, tmp, 1);

        rule_vand(model.labels[1].truthtable, model.labels[1].truthtable, tmp, model.nsamples, &temp);

        rule_vfree(&tmp);
#endif

        PermutationMap * p;
        if(useCapturedPMap)
            p = new CapturedPermutationMap();
        else
            p = new PrefixPermutationMap();

        CacheTree * tree = new CacheTree(model.nsamples, model.ntotal_rules, model.c, model.rules, model.labels, model.minority, ablation, false, "node");
        Queue * q = new Queue(q_cmp, "run type");

        // Run CORELS
        bbound(tree, max_num_nodes, q, p);
        double c_obj = tree->min_objective();

        // Evaluate CORELS objective to make sure it corresponds to the correct rule list outputted as well
        tracking_vector<unsigned short, DataStruct::Tree> opt_list = tree->opt_rulelist();
        tracking_vector<bool, DataStruct::Tree> opt_preds = tree->opt_predictions();
        tracking_vector<int, DataStruct::Tree> opt_preds_int(opt_preds.begin(), opt_preds.end());

        model.nrules = opt_list.size();
        model.ids = &opt_list[0];

        model.predictions = &opt_preds_int[0];
        model.default_prediction = opt_preds_int[model.nrules];

        double e_obj = evaluate(model, v);


        tracking_vector<unsigned short, DataStruct::Tree> b_opt_list;
        tracking_vector<bool, DataStruct::Tree> b_opt_preds;

        double b_obj = obj_brute(&model, b_max_list_len, v);

        // Get optimal rule list info generated by brute force
        b_opt_list.assign(model.ids, model.ids + model.nrules);
        b_opt_preds.assign(model.predictions, model.predictions + model.nrules);
        b_opt_preds.push_back(model.default_prediction);

        if(e_obj == -1.0) {
            if(v > 0)
                printf("[main] Error with evaluation calculations! Exiting\n");

            returnCode = 2;
            exit = true;
        }


        if(b_obj == -1.0) {
            if(v > 0)
                printf("[main] Error with objective calculations! Exiting\n");

            returnCode = 2;
            exit = true;
        }

        double d = c_obj - e_obj;
        double d1 = c_obj - b_obj;
        double e = epsilon;

        if(d1 > e || d > e || d < -e) {
            if(v > 1) {
                printf("[main] Mismatch detected, logging and exiting\n");
            }

            output_error(model, opt_list, opt_preds, b_opt_list, b_opt_preds, c_obj, e_obj, b_obj, v);

            returnCode = 1;
            exit = true;
        }


        delete p;

        if(c_obj == 0.0)
            tree->insert_root();

        delete tree;
        delete q;
    }

    model_free(model);

#ifdef GMP
    gmp_randclear(rand_state);
#endif

    return returnCode;
}
