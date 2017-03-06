#pragma once

#include "rule.h"

#include <cstdlib>
#include <sys/time.h>
#include <string.h>
#include <stdio.h>
#include <fstream>
#include <vector>
//#include <gmpxx.h>

using namespace std;

class Logger {
  public:
    void closeFile() { if (_f.is_open()) _f.close(); }
    ~Logger() { 
        free(_state.prefix_lens);
        closeFile(); 
    }

    void setLogFileName(char *fname);
    void dumpState();
    std::string dumpPrefixLens();
    std::string dumpRemainingSpaceSize();
    size_t dumpLogRemainingSpaceSize();

    inline void setVerbosity(int verbosity) {
        _v = verbosity;
    }
    inline void setFrequency(int frequency) {
        _freq = frequency;
    }
    inline int getFrequency() {
        return _freq;
    }
    inline void setLowerBoundTime(double t) {
        _state.lower_bound_time = t;
    }
    inline void incLowerBoundNum() {
        ++_state.lower_bound_num;
    }
    inline void addToObjTime(double t) {
        _state.objective_time += t;
    }
    inline void incObjNum() {
        ++_state.objective_num;
    }
    inline void addToTreeInsertionTime(double t) {
        _state.tree_insertion_time += t;
    }
    inline void incTreeInsertionNum() {
        ++_state.tree_insertion_num;
    }
    inline void addToRuleEvalTime(double t) {
        _state.rule_evaluation_time += t;
    }
    inline void incRuleEvalNum() {
        ++_state.rule_evaluation_num;
    }
    inline void addToNodeSelectTime(double t) {
        _state.node_select_time += t;
    }
    inline void incNodeSelectNum() {
        ++_state.node_select_num;
    }
    inline void addToEvalChildrenTime(double t) {
        _state.evaluate_children_time += t;
    }
    inline void incEvalChildrenNum() {
        ++_state.evaluate_children_num;
    }
    inline void setInitialTime(double t) {
        _state.initial_time = t;
    }
    inline double getInitialTime() {
        return _state.initial_time;
    }
    inline void setTotalTime(double t) {
        _state.total_time = t;
    }
    inline void addToPermMapInsertionTime(double t) {
        _state.permutation_map_insertion_time += t;
    }
    inline void incPermMapInsertionNum() {
        ++_state.permutation_map_insertion_num;
    }
    inline void setCurrentLowerBound(double lb) {
        _state.current_lower_bound = lb;
    }
    inline void setTreeMinObj(double o) {
        _state.tree_min_objective = o;
    }
    inline void setTreePrefixLen(size_t n) {
        _state.tree_prefix_length = n;
    }
    inline void setTreeNumNodes(size_t n) {
        _state.tree_num_nodes = n;
    }
    inline void setTreeNumEvaluated(size_t n) {
        _state.tree_num_evaluated = n;
    }
    inline void setTreeNodeSize(size_t n) {
        _state.tree_node_size = n;
    }
    inline size_t getTreeMemory() {
        return _state.tree_num_nodes * _state.tree_node_size;
    }
    inline void setQueueSize(size_t n) {
        _state.queue_size = n;
    }
    inline void setNRules(size_t nrules) {
        _state.nrules = nrules - 1;     // the first rule is the default rule
    }
    inline void setC(double c) {
        _state.c = c;
    }
    inline void initPrefixVec() {
        _state.prefix_lens = (size_t*) calloc(_state.nrules, sizeof(size_t));
    }
    inline void incPrefixLen(size_t n) {
        ++_state.prefix_lens[n];
        if (_state.prefix_lens[n] == 1)
            updateQueueMinLen();
    }
    inline void decPrefixLen(size_t n) {
        --_state.prefix_lens[n];
        if (_state.prefix_lens[n] == 0)
            updateQueueMinLen();
    }
    inline size_t sumPrefixLens() { // size of logical queue
        size_t tot = 0;
        for(size_t i = 0; i < _state.nrules; ++i) {
            tot += _state.prefix_lens[i];
        }
        return tot;
    }
    inline void updateQueueMinLen() {
        size_t min_length = 0; // note that min length is logically undefined when queue size is 0
        for(size_t i = 0; i < _state.nrules; ++i) {
            if (_state.prefix_lens[i] > 0) {
                min_length = i;
                break;
            }
        }
        _state.queue_min_length = min_length;
    }
    inline size_t getQueueMinLen() {
        return _state.queue_min_length;
    }
    inline void incPmapSize() {
        ++_state.pmap_size;
    }
    inline void decreasePmapSize(size_t n) {
        _state.pmap_size -= n;
    }
    inline void incPmapNullNum() {
        ++_state.pmap_null_num;
    }
    inline void incPmapDiscardNum() {
        ++_state.pmap_discard_num;
    }
    inline void setPmapNodeSize(size_t n) {
        _state.pmap_node_size = n;
    }
    inline size_t getPmapMemory() {
        return _state.pmap_node_size * _state.pmap_size;
    }
    inline void subtreeSize(mpz_t tot, unsigned int len_prefix, double lower_bound) {
        // theorem 4 (fine-grain upper bound on number of remaining prefix evaluations)
        unsigned int f_naive = _state.nrules - len_prefix;
        unsigned int f = (_state.tree_min_objective - lower_bound) / _state.c;
        if (f_naive < f)
            f = f_naive;
        mpz_set_ui(tot, _state.nrules - len_prefix);
        for (unsigned int k = (_state.nrules - len_prefix - 1); k >= (_state.nrules - len_prefix - f + 1); k--) {
            mpz_addmul_ui(tot, tot, k);
        }
    }
    inline void addQueueElement(unsigned int len_prefix, double lower_bound) {
        mpz_t tot;
        mpz_init(tot);
        subtreeSize(tot, len_prefix, lower_bound);
        mpz_add(_state.remaining_space_size, _state.remaining_space_size, tot);
        mpz_clear(tot);
    }
    inline void removeQueueElement(unsigned int len_prefix, double lower_bound) {
        mpz_t tot;
        mpz_init(tot);
        subtreeSize(tot, len_prefix, lower_bound);
        mpz_sub(_state.remaining_space_size, _state.remaining_space_size, tot);
        mpz_clear(tot);
    }
    inline void initRemainingSpaceSize() {
        // proposition 2 (upper bound on total number of prefix evaluations)
        size_t naive_max_length = 0.5 / _state.c;
        if (naive_max_length < _state.nrules)
            mpz_fac_ui(_state.remaining_space_size, naive_max_length);
        else
            mpz_fac_ui(_state.remaining_space_size, _state.nrules);
    }
    inline void clearRemainingSpaceSize() {
        mpz_set_ui(_state.remaining_space_size, 0);
    }
    inline size_t getLogRemainingSpaceSize() {
        return mpz_sizeinbase(_state.remaining_space_size, 10); // this is approximate
    }
    inline void initializeState() { // initialize so we can write a log record immediately
        _state.total_time = 0.;
        _state.evaluate_children_time = 0.;
        _state.evaluate_children_num = 0;
        _state.node_select_time = 0.;
        _state.node_select_num = 0;
        _state.rule_evaluation_time = 0.;
        _state.rule_evaluation_num = 0;
        _state.lower_bound_time = 0.;
        _state.lower_bound_num = 0;
        _state.objective_time = 0.;
        _state.objective_num = 0;
        _state.tree_insertion_time = 0.;
        _state.tree_insertion_num = 0;
        _state.permutation_map_insertion_time = 0.;
        _state.permutation_map_insertion_num = 0;
        _state.current_lower_bound = 0.;
        _state.tree_min_objective = 1.;
        _state.tree_prefix_length = 0;
        _state.tree_num_nodes = 0;
        _state.tree_num_evaluated = 0;
        _state.tree_node_size = 0;
        _state.tree_memory = 0;
        _state.queue_size = 0;
        _state.queue_min_length = 0;
        _state.queue_memory = 0;
        _state.pmap_size = 0;
        _state.pmap_null_num = 0;
        _state.pmap_discard_num = 0;
        _state.pmap_memory = 0;
        mpz_init(_state.remaining_space_size);
        initRemainingSpaceSize();
    }


  private:
    struct State {
        size_t nrules;
        double c;
        double initial_time;                    // initial time stamp
        double total_time;
        double evaluate_children_time;
        size_t evaluate_children_num;
        double node_select_time;
        size_t node_select_num;
        double rule_evaluation_time;
        size_t rule_evaluation_num;
        double lower_bound_time;
        size_t lower_bound_num;
        double objective_time;
        size_t objective_num;
        double tree_insertion_time;
        size_t tree_insertion_num;
        double permutation_map_insertion_time;
        size_t permutation_map_insertion_num;   // number of calls to `permutation_insert` function
        double current_lower_bound;             // monotonically decreases for curious lower bound policy
        double tree_min_objective;
        size_t tree_prefix_length;
        size_t tree_num_nodes;
        size_t tree_num_evaluated;
        size_t tree_node_size;
        size_t tree_memory;
        size_t queue_size;
        size_t queue_min_length;                // monotonically increases
        size_t queue_memory;
        size_t pmap_size;                       // size of pmap
        size_t pmap_null_num;                   // number of pmap lookup operations that return null
        size_t pmap_discard_num;                // number of pmap lookup operations that trigger discard
        size_t pmap_node_size;
        size_t pmap_memory;
        size_t* prefix_lens;
        mpz_t remaining_space_size;
    };
    State _state;
    int _v; // verbosity
    int _freq; // frequency of logging
    ofstream _f; // output file
};

inline double timestamp() {
    struct timeval now;
    gettimeofday(&now, 0);
    return now.tv_sec + now.tv_usec * 0.000001;
}

inline double time_diff(double t0) {
    return timestamp() - t0;
}

// rulelist -- rule ids of optimal rulelist
// preds -- corresponding predictions of rules (+ default prediction)
void print_final_rulelist(const std::vector<unsigned short>& rulelist,
                          const std::vector<bool>& preds,
                          const bool latex_out,
                          const rule_t rules[],
                          const rule_t labels[],
                          char fname[]);

extern Logger logger;

void print_machine_info();

