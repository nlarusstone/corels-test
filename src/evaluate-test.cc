#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "queue.hh"
#include "evaluate.hh"

NullLogger * logger;

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

int main(int argc, char ** argv)
{
    model_t model;

    /** TWEAKING PARAMETERS **/

    model.ntotal_rules = 200;
    model.nlabels = 2;
    model.nsamples = 1000;
    model.c = 0.015;

    double v = 5;

    int b_max_list_len = 2;

    // CORELS stuff
    int ablation = 2;
    std::function<bool(Node*, Node*)> q_cmp = lb_cmp;
    bool useCapturedPMap = false;

    size_t max_num_nodes = 1000000;

    // General stuff
    size_t num_iters = 1000000;

    double epsilon = 0.000000001;

    unsigned long seed = time(NULL);

    /************************/

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
    logger = new NullLogger();

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

    delete logger;

    return returnCode;
}
