#include "rule.h"
#include <iostream>
#include <set>

void run_corels (bool run_bfs, int max_num_nodes, double c, std::set<std::string> verbosity,
                    int curiosity_policy, int map_type, int freq, int ablation, bool calculate_size,
                    bool latex_out, int nrules, int nlabels, int nsamples, rule_t *rules,
                    rule_t *labels, rule_t *meta);
