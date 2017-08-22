#include "run.hh"
#include <stdio.h>
#include <getopt.h>
#include <string.h>
#include <map>

#define BUFSZ 512

int main(int argc, char *argv[]) {
    const char usage[] = "USAGE: %s [-b] "
        "[-n max_num_nodes] [-r regularization] [-v (rule|label|samples|progress|log|silent)] "
        "-c (1|2|3|4) -p (0|1|2) [-f logging_frequency] "
        "-a (0|1|2) [-s] [-L latex_out] "
        "data.out data.label [data.minor]\n\n"
        "%s\n";

    extern char *optarg;
    bool run_bfs = false;
    bool run_curiosity = false;
    int curiosity_policy = 0;
    bool latex_out = false;
    char *vopt;
    std::set<std::string> verbosity;
    bool verr = false;
    const char *vstr = "rule|label|samples|progress|log|silent";
    int map_type = 0;
    int max_num_nodes = 100000;
    double c = 0.01;
    char ch;
    bool error = false;
    char error_txt[BUFSZ];
    int freq = 1000;
    int ablation = 0;
    bool calculate_size = false;
    /* only parsing happens here */
    while ((ch = getopt(argc, argv, "bsLc:p:v:n:r:f:a:")) != -1) {
        switch (ch) {
        case 'b':
            run_bfs = true;
            break;
        case 's':
            calculate_size = true;
            break;
        case 'c':
            run_curiosity = true;
            curiosity_policy = atoi(optarg);
            break;
        case 'L':
            latex_out = true;
            break;
        case 'p':
            map_type = atoi(optarg);
            break;
        case 'v':
            vopt = strtok(optarg, ",");
            while (vopt != NULL) {
                if (!strstr(vstr, vopt)) {
                    verr = true;
                    break;
                }
                verbosity.insert(vopt);
                vopt = strtok(NULL, ",");
            }
            break;
        case 'n':
            max_num_nodes = atoi(optarg);
            break;
        case 'r':
            c = atof(optarg);
            break;
        case 'f':
            freq = atoi(optarg);
            break;
        case 'a':
            ablation = atoi(optarg);
            break;
        default:
            error = true;
            snprintf(error_txt, BUFSZ, "unknown option: %c", ch);
        }
    }
    if (max_num_nodes < 0) {
        error = true;
        snprintf(error_txt, BUFSZ, "number of nodes must be positive");
    }
    if (c < 0) {
        error = true;
        snprintf(error_txt, BUFSZ, "regularization constant must be postitive");
    }
    if (map_type > 2 || map_type < 0) {
        error = true;
        snprintf(error_txt, BUFSZ, "symmetry-aware map must be (0|1|2)");
    }
    if ((run_bfs + run_curiosity) != 1) {
        error = true;
        snprintf(error_txt, BUFSZ,
                "you must use exactly one of (-b | -c)");
    }
    if (argc < 2 + optind) {
        error = true;
        snprintf(error_txt, BUFSZ,
                "you must specify data files for rules and labels");
    }
    if (run_curiosity && !((curiosity_policy >= 1) && (curiosity_policy <= 4))) {
        error = true;
        snprintf(error_txt, BUFSZ,
                "you must specify a curiosity type (1|2|3|4)");
    }
    if (verr) {
        error = true;
        snprintf(error_txt, BUFSZ,
                 "verbosity options must be one or more of (rule|label|samples|progress|log|silent), separated with commas (i.e. -v progress,log)");
    }
    if (verbosity.count("samples") && !(verbosity.count("rule") || verbosity.count("label"))) {
        error = true;
        snprintf(error_txt, BUFSZ,
                 "verbosity 'samples' option must be combined with at least one of (rule|label)");
    }
    if (verbosity.size() > 2 && verbosity.count("silent")) {
        snprintf(error_txt, BUFSZ,
                 "verbosity 'silent' option must be passed without any additional verbosity parameters");
    }

    if (error) {
        fprintf(stderr, usage, argv[0], error_txt);
        return 1;
    }

    // default: show progress
    if (verbosity.size() == 0) {
        verbosity.insert("progress");
    }

    if (verbosity.count("silent")) {
        verbosity.clear();
    }

    argc -= optind;
    argv += optind;

    int nrules, nsamples, nlabels, nsamples_chk;
    rule_t *rules, *labels;
    rules_init(argv[0], &nrules, &nsamples, &rules, 1);
    rules_init(argv[1], &nlabels, &nsamples_chk, &labels, 0);

    int nmeta, nsamples_check;
    // Equivalent points information is precomputed, read in from file, and stored in meta
    rule_t *meta;
    if (argc == 3)
        rules_init(argv[2], &nmeta, &nsamples_check, &meta, 0);
    else
        meta = NULL;

    char froot[BUFSZ];
    char log_fname[BUFSZ];
    char opt_fname[BUFSZ];
    const char* pch = strrchr(argv[0], '/');
    snprintf(froot, BUFSZ, "../logs/for-%s-%s%s-%s-%s-removed=%s-max_num_nodes=%d-c=%.7f-f=%d",
            pch ? pch + 1 : "",
            run_bfs ? "bfs" : "",
            run_curiosity ? curiosity_map[curiosity_policy].c_str() : "",
            (map_type == 1) ? "with_prefix_perm_map" :
                (map_type == 2 ? "with_captured_symmetry_map" : "no_pmap"),
            meta ? "minor" : "no_minor",
            ablation ? ((ablation == 1) ? "support" : "lookahead") : "none",
            max_num_nodes, c, freq);
    snprintf(log_fname, BUFSZ, "%s.txt", froot);
    snprintf(opt_fname, BUFSZ, "%s-opt.txt", froot);

    run_corels(opt_fname, log_fname, max_num_nodes, c, verbosity, curiosity_policy, map_type,
                    freq, ablation, calculate_size, latex_out, nrules, nlabels,
                    nsamples, rules, labels, meta);

    if (meta) {
        if (verbosity.count("progress"))
            printf("\ndelete identical points indicator");
        rules_free(meta, nmeta, 0);
    }

    if (verbosity.count("progress")) {
        printf("\ndelete rules\n");
    }
    rules_free(rules, nrules, 1);

    if (verbosity.count("progress")) {
        printf("delete labels\n");
    }
    rules_free(labels, nlabels, 0);

    return 0;
}
