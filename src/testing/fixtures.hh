#pragma once

#define PERM_MAP_TESTS
#include "../queue.hh"

#ifdef GMP
    #include <gmp.h>
#else
    #define NENTRIES  ((nsamples + (int)BITS_PER_ENTRY - 1) / (int)BITS_PER_ENTRY)
#endif

extern rule_t * rules;
extern rule_t * labels;
extern rule_t * minority;
extern int nrules;
extern int nsamples;
extern int nlabels;
extern int nminority;


class TrieFixture {

public:
    TrieFixture() : c(0.01), type("node"), ablation(0), calculate_size(false),
                    tree(NULL), root(NULL) {
        tree = new CacheTree(nsamples, nrules, c, rules, labels,
                                 minority, ablation, calculate_size, type);

        if(tree) {
            tree->insert_root();
            root = tree->root();
        }
    }

    virtual ~TrieFixture() {
        if(tree)
            delete tree;
    }

protected:
    double c;
    const char * type;
    int ablation;
    bool calculate_size;
    CacheTree * tree;
    Node * root;
};


class PrefixMapFixture {

public:
    PrefixMapFixture() : pmap(NULL), tree(NULL), root(NULL), num_not_captured(0),
                         c(0.01), prediction(true), default_prediction(true),
                         lower_bound(0.1), objective(0.5), len_prefix(4), equivalent_minority(0.0) {
        pmap = new PrefixPermutationMap();

        tree = new CacheTree(nsamples, nrules, c, rules, labels, NULL, 0, false, "node");

        if(tree) {
            tree->insert_root();
            root = tree->root();
        }

        correct_key = {4, 1, 2, 4, 5};

        parent_prefix = {4, 2, 1};
        new_rule = 5;
        correct_indices = {4, 2, 1, 0, 3};

        // For second and third tests
        parent_prefix_2 = {1, 4, 5};
        new_rule_2 = 2;
        correct_indices_2 = {4, 0, 3, 1, 2};
    }

    virtual ~PrefixMapFixture() {
        if(pmap)
            delete pmap;

        if(tree)
            delete tree;
    }

protected:

    PrefixPermutationMap * pmap;
    CacheTree * tree;
    Node * root;

    int num_not_captured;

    double c;

    bool prediction;
    bool default_prediction;
    double lower_bound;
    double objective;
    int len_prefix;

    std::vector<unsigned short> correct_key;

    tracking_vector<unsigned short, DataStruct::Tree> parent_prefix;
    int new_rule;
    std::vector<unsigned char> correct_indices;

    tracking_vector<unsigned short, DataStruct::Tree> parent_prefix_2;
    int new_rule_2;
    std::vector<unsigned char> correct_indices_2;

    double equivalent_minority;
};


class CapturedMapFixture {

public:
    CapturedMapFixture() : pmap(NULL), tree(NULL), root(NULL), num_not_captured(0),
                         c(0.01), prediction(true), default_prediction(true),
                         lower_bound(0.1), objective(0.5), len_prefix(4), equivalent_minority(0.0) {
        pmap = new CapturedPermutationMap();

        tree = new CacheTree(nsamples, nrules, c, rules, labels, NULL, 0, false, "node");

        if(tree) {
            tree->insert_root();
            root = tree->root();
        }

        parent_prefix = {4, 2, 1};
        new_rule = 5;

        // For second and third tests
        parent_prefix_2 = {1, 4, 5};
        new_rule_2 = 2;

        std::vector<unsigned short> ordered_prefix = {1, 2, 4, 5};

        rule_vinit(nsamples, &not_captured);

#ifdef GMP
        for(size_t i = 0; i < ordered_prefix.size(); i++) {
            mpz_ior(not_captured, not_captured, rules[ordered_prefix.at(i)].truthtable);
        }

        mpz_com(not_captured, not_captured);
#else
        for(int i = 0; i < NENTRIES; i++) {
            not_captured[i] = ~(not_captured[i] & 0);
        }

        for(size_t i = 0; i < ordered_prefix.size(); i++) {
            for(int j = 0; j < NENTRIES; j++) {
                not_captured[j] = not_captured[j] & ~(rules[ordered_prefix.at(i)].truthtable[j]);
            }
        }
#endif
    }

    virtual ~CapturedMapFixture() {
        rule_vfree(&not_captured);

        if(pmap)
            delete pmap;

        if(tree)
            delete tree;
    }

protected:

    CapturedPermutationMap * pmap;
    CacheTree * tree;
    Node * root;

    int num_not_captured;

    double c;

    bool prediction;
    bool default_prediction;
    double lower_bound;
    double objective;
    int len_prefix;

    VECTOR not_captured;

    tracking_vector<unsigned short, DataStruct::Tree> parent_prefix;
    int new_rule;

    tracking_vector<unsigned short, DataStruct::Tree> parent_prefix_2;
    int new_rule_2;

    double equivalent_minority;
};


class QueueFixture {

public:
    QueueFixture() : queue(NULL), tree(NULL), root(NULL) {
        queue = new Queue(lb_cmp, "LOWER BOUND");

        tree = new CacheTree(nsamples, nrules, 0.01, rules, labels, NULL, 0, false, "node");

        if(tree) {
            tree->insert_root();
            root = tree->root();
        }
    }

    virtual ~QueueFixture() {
        if(queue)
            delete queue;

        if(tree)
            delete tree;
    }

protected:

    Queue * queue;
    CacheTree * tree;
    Node * root;
};
