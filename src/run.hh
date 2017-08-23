#pragma once

#include "rule.h"

#ifdef __cplusplus
extern "C" {
#endif

int run_corels (char* opt_file, char* log_file,
                 int max_num_nodes, double c, char* vstring, int curiosity_policy, int map_type,
                 int freq, int ablation, int calculate_size, int latex_out, int nrules, int nlabels, int nsamples,
                 rule_t * rules, rule_t * labels, rule_t * meta);

#ifdef __cplusplus
}
#endif
