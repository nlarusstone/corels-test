#include <stdio.h>
#include <iostream>
#include <set>

#include "queue.hh"
#include "run.hh"

#define BUFSZ 512

NullLogger* logger;

extern "C" {

int run_corels (char* opt_file, char* log_file,
                 int max_num_nodes, double c, char* vstring, int curiosity_policy, int map_type,
                 int freq, int ablation, int calculate_size, int latex_out, int nrules, int nlabels, int nsamples,
                 rule_t * rules, rule_t * labels, rule_t * meta) {

    printf("ran\n");

    std::set<std::string> verbosity;

    const char* voptions = "rule|label|samples|progress|log|silent";

    char* vopt = strtok(vstring, ",");
    while (vopt != NULL) {
        if (!strstr(voptions, vopt)) {
            fprintf(stderr, "verbosity options must be one or more of (rule|label|samples|progress|log|silent), separated with commas (i.e. -v progress,log)");
            return 1;
        }
        verbosity.insert(vopt);
        vopt = strtok(NULL, ",");
    }

    if (verbosity.count("samples") && !(verbosity.count("rule") || verbosity.count("label"))) {
        fprintf(stderr, "verbosity 'samples' option must be combined with at least one of (rule|label)");
        return 1;
    }
    if (verbosity.size() > 2 && verbosity.count("silent")) {
        fprintf(stderr, "verbosity 'silent' option must be passed without any additional verbosity parameters");
        return 1;
    }

    if (verbosity.size() == 0) {
        verbosity.insert("progress");
    }

    if (verbosity.count("silent")) {
        verbosity.clear();
    }

    if (verbosity.count("log"))
        print_machine_info();

    if (verbosity.count("rule")) {
        printf("\n%d rules %d samples\n\n", nrules, nsamples);
        rule_print_all(rules, nrules, nsamples, (verbosity.count("samples")));
    }

    if (verbosity.count("label")) {
        printf("\nLabels (%d) for %d samples\n\n", nlabels, nsamples);
        rule_print_all(labels, nlabels, nsamples, (verbosity.count("samples")));
    }

    printf("verbosity\n");

    if (verbosity.count("log")) {
        logger = new Logger(c, nrules, verbosity, log_file, freq);
    } else {
        logger = new NullLogger();
        logger->setVerbosity(verbosity);
    }
    printf("logger\n");   
    double init = timestamp();
    char run_type[BUFSZ];
    Queue* q;
    strcpy(run_type, "LEARNING RULE LIST via ");
    char const *type = "node";
    if (curiosity_policy == 1) {
        strcat(run_type, "CURIOUS");
        q = new Queue(curious_cmp, run_type);
        type = "curious";
    } else if (curiosity_policy == 2) {
        strcat(run_type, "LOWER BOUND");
        q = new Queue(lb_cmp, run_type);
    } else if (curiosity_policy == 3) {
        strcat(run_type, "OBJECTIVE");
        q = new Queue(objective_cmp, run_type);
    } else if (curiosity_policy == 4) {
        strcat(run_type, "DFS");
        q = new Queue(dfs_cmp, run_type);
    } else {
        strcat(run_type, "BFS");
        q = new Queue(base_cmp, run_type);
    }

    PermutationMap* p;
    if (map_type == 1) {
        strcat(run_type, " Prefix Map\n");
        PrefixPermutationMap* prefix_pmap = new PrefixPermutationMap;
        p = (PermutationMap*) prefix_pmap;
    } else if (map_type == 2) {
        strcat(run_type, " Captured Symmetry Map\n");
        CapturedPermutationMap* cap_pmap = new CapturedPermutationMap;
        p = (PermutationMap*) cap_pmap;
    } else {
        strcat(run_type, " No Permutation Map\n");
        NullPermutationMap* null_pmap = new NullPermutationMap;
        p = (PermutationMap*) null_pmap;
    }

    CacheTree* tree = new CacheTree(nsamples, nrules, c, rules, labels, meta, ablation, calculate_size, type);
    if (verbosity.count("progress"))
        printf("%s", run_type);
    // runs our algorithm
    bbound(tree, max_num_nodes, q, p);

    const tracking_vector<unsigned short, DataStruct::Tree>& r_list = tree->opt_rulelist();

    if (verbosity.count("progress")) {
        printf("final num_nodes: %zu\n", tree->num_nodes());
        printf("final num_evaluated: %zu\n", tree->num_evaluated());
        printf("final min_objective: %1.5f\n", tree->min_objective());
        printf("final accuracy: %1.5f\n",
           1 - tree->min_objective() + c*r_list.size());
   }

    print_final_rulelist(r_list, tree->opt_predictions(),
                     latex_out, rules, labels, opt_file, verbosity.count("progress"));

    if (verbosity.count("progress"))
        printf("final total time: %f\n", time_diff(init));

    logger->dumpState();
    logger->closeFile();

    if (verbosity.count("progress")) {
        printf("\ndelete tree\n");
    }
    delete tree;

    if (verbosity.count("progress")) {
        printf("\ndelete symmetry-aware map\n");
    }
    delete p;

    if (verbosity.count("progress")) {
        printf("\ndelete priority queue\n");
    }
    delete q;

    /*if (verbosity.count("progress")) {
        printf("\ndelete logger\n");
    }
    delete logger;*/

    return 0;
}

} // end extern C
