#include "queue.hh"
#include "evaluate.hh"

NullLogger * logger;

int main(int argc, char ** argv)
{
    const char * model_file = NULL; //"../logs/for-evaluate.out-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=100000-c=0.0150000-v=0-f=1000-opt.txt";
    const char * out_file = "../data/evaluate-data/evaluate.out";
    const char * label_file = "../data/evaluate-data/evaluate.label";
    const char * minor_file = NULL; //"../data/evaluate-data/evaluate.minor";
    double c = 0.015;
    double v = 5;

    int ablation = 2;
    std::function<bool(Node*, Node*)> q_cmp = lb_cmp;
    bool useCapturedPMap = false;
    size_t max_num_nodes = 1000000;
    size_t num_iters = 100;

    int returnCode = 0;
    logger = new NullLogger();


    model_t model;
    if(model_init(&model, model_file, out_file, label_file, minor_file, c, v) != 0) {
        delete logger;
        return 1;
    }

    unsigned long seed = time(NULL);

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

        printf("number of ones: %d\n", temp);

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

        if(e_obj == -1.0) {
            if(v > 0)
                printf("[main] Error with evaluation calculations! Exiting\n");

            returnCode = 2;
            exit = true;
        }

        double d = c_obj - e_obj;
        double e = 0.0000001;

        if(d < e && d > -e) {
            if(v > 2)
                printf("[main] Minimum objective and optimal rule list match!\n");
        }
        else if(v > 1) {
            printf("[main] ERROR: Mismatch of minimum objective and optimal rule list:\n" \
                "[main]     corels obj: %.10f    evaluate (optimal rule list) obj: %.10f\n",
                c_obj, e_obj);

            print_final_rulelist(opt_list, opt_preds,
                             NULL, model.rules, model.labels, NULL);

            returnCode = 1;
            exit = true;
        }

        model.nrules = 0;

        // Run brute force
        double b_obj = obj_brute(model, v);

        if(b_obj == -1.0) {
            if(v > 0)
                printf("[main] Error with objective calculations! Exiting\n");

            returnCode = 2;
            exit = true;
        }

        double d1 = c_obj - b_obj;
        double e1 = 0.0000001;

        if(d1 < e1 && d1 > -e1) {
            if(v > 2)
                printf("[main] Minimum objectives match!\n");
        }
        else if(v > 1) {
            printf("[main] ERROR: Mismatch of minimum objectives:\n" \
                "[main]     corels obj: %.10f    brute-force obj: %.10f\n",
                c_obj, b_obj);

            print_final_rulelist(opt_list, opt_preds,
                             NULL, model.rules, model.labels, NULL);

            returnCode = 1;
            exit = true;
        }

        delete p;
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
