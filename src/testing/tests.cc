/***  MAIN FILE WITH THE ACTUAL TESTS ***/

#define PREFIX_MAP_TESTS
#include "../queue.hh"

#ifdef GMP
#include <gmp.h>
#endif

#include "catch.hpp"

extern rule_t * rules;
extern rule_t * labels;
extern rule_t * minority;
extern int nrules;
extern int nsamples;
extern int nlabels;
extern int nminority;

// TODO: Add curiosity checks

TEST_CASE("Test trie", "[trie]") {
    double c = 0.01;
    const char * type = "node";
    int ablation = 0;
    bool calculate_size = false;
    CacheTree * tree = new CacheTree(nsamples, nrules, c, rules, labels,
                                     minority, ablation, calculate_size, type);

    REQUIRE_FALSE(tree == NULL);

    tree->insert_root();
    Node * root = tree->root();

    REQUIRE_FALSE(root == NULL);

    SECTION("Test tree initialization") {

        CHECK(tree->num_nodes() == 1);
        CHECK(tree->num_evaluated() == 0);
        CHECK(tree->c() == c);
        CHECK(tree->nsamples() == nsamples);
        CHECK(tree->nrules() == nrules);
        CHECK(tree->ablation() == ablation);
        CHECK(tree->has_minority() == (bool)minority);
        CHECK(tree->calculate_size() == calculate_size);

        for(int i = 0; i < nrules; i++) {
            CAPTURE(i);
            CHECK(tree->rule(i).support == rules[i].support);
            CHECK(tree->rule(i).cardinality == rules[i].cardinality);
            CHECK(std::string(tree->rule(i).features) == std::string(rules[i].features));
            CHECK(std::string(tree->rule_features(i)) == std::string(rules[i].features));

#ifdef GMP
            CHECK(mpz_cmp(tree->rule(i).truthtable, rules[i].truthtable) == 0);
#else
            for(int j = 0; j < nsamples; j++) {
                CAPTURE(j);
                CHECK(tree->rule(i).truthtable[j] == rules[i].truthtable[j]);
            }
#endif
        }

        for(int i = 0; i < nlabels; i++) {
            CAPTURE(i);
            CHECK(tree->label(i).support == labels[i].support);
            CHECK(tree->label(i).cardinality == labels[i].cardinality);
            CHECK(std::string(tree->label(i).features) == std::string(labels[i].features));

#ifdef GMP
            CHECK(mpz_cmp(tree->label(i).truthtable, labels[i].truthtable) == 0);
#else
            for(int j = 0; j < nsamples; j++) {
                CAPTURE(j);
                CHECK(tree->label(i).truthtable[j] == label[i].truthtable[j]);
            }
#endif
        }

        // TODO: Fix minority checks
        if(minority != NULL) {
            for(int i = 0; i < nminority; i++) {
                CAPTURE(i);
                CHECK(tree->minority(i).support == minority[i].support);
                CHECK(tree->minority(i).cardinality == minority[i].cardinality);
                CHECK(std::string(tree->minority(i).features) == std::string(minority[i].features));

#ifdef GMP
                CHECK(mpz_cmp(tree->minority(i).truthtable, minority[i].truthtable) == 0);
#else
                for(int j = 0; j < nsamples; j++) {
                    CAPTURE(j);
                    CHECK(tree->minority(i).truthtable[j] == minority[i].truthtable[j]);
                }
#endif
            }
        }
    }

    SECTION("Construct and insert node") {

        Node * parent = root;

        REQUIRE_FALSE(parent == NULL);

        unsigned short rule_id = 1;
        bool prediction = true;
        bool default_prediction = true;
        double lower_bound = 0.1;
        double objective = 0.12;
        int num_not_captured = 5;
        int len_prefix = 0;
        double equivalent_minority = 0.1;

        Node * n = tree->construct_node(rule_id, nrules, prediction, default_prediction,
                                        lower_bound, objective, parent,
                                        num_not_captured, nsamples, len_prefix,
                                        c, equivalent_minority);

        REQUIRE_FALSE(n == NULL);

        CHECK(n->id() == rule_id);
        CHECK(n->prediction() == prediction);
        CHECK(n->default_prediction() == default_prediction);
        CHECK(n->lower_bound() == lower_bound);
        CHECK(n->objective() == objective);
        CHECK(n->num_captured() == (nsamples - num_not_captured));
        CHECK(n->depth() == (len_prefix + 1));
        CHECK(n->equivalent_minority() == equivalent_minority);
        CHECK_FALSE(n->deleted());
        CHECK(n->depth() == 1);

        tree->insert(n);

        CHECK(tree->num_nodes() == 2);

        CHECK(n->parent() == parent);
        CHECK(parent->children_begin()->second == n);
        CHECK(parent->num_children() == 1);
        CHECK(parent->child(rule_id) == n);
    }

    SECTION("Check node delete behavior") {

        Node * n = tree->construct_node(1, nrules, true, true, 0.1, 0.12, root, 3, nsamples, 0, 0.01, 0.0);

        REQUIRE_FALSE(n == NULL);

        tree->insert(n);

        n->set_deleted();
        CHECK(n->deleted());

        root->delete_child(1);

        CHECK(root->num_children() == 0);

        CHECK(tree->num_nodes() == 1);
    }

    SECTION("Node get prefix and predictions") {
        Node * n = root;
        int depth = 3;

        tracking_vector<unsigned short, DataStruct::Tree> prefix;
        tracking_vector<bool, DataStruct::Tree> predictions;

        for(int i = 0; i < depth; i++) {
            n = tree->construct_node(i+1, nrules, (bool)(i % 2), true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
            tree->insert(n);

            prefix.push_back(i+1);
            predictions.push_back((bool)(i % 2));
        }

        REQUIRE(tree->num_nodes() == (depth + 1));
        REQUIRE(n->depth() == depth);

        std::pair<tracking_vector<unsigned short, DataStruct::Tree>, tracking_vector<bool, DataStruct::Tree>> p =
            n->get_prefix_and_predictions();

        CHECK(p.first == prefix);
        CHECK(p.second == predictions);
    }

    SECTION("Increment num evaluated") {

        size_t num = tree->num_evaluated();
        tree->increment_num_evaluated();

        REQUIRE(tree->num_evaluated() == (num + 1));
    }

    SECTION("Decrement num nodes") {

        Node * n = tree->construct_node(1, nrules, true, true, 0.1, 0.12, root, 3, nsamples, 0, 0.01, 0.0);

        REQUIRE_FALSE(n == NULL);

        tree->insert(n);

        REQUIRE(tree->num_nodes() == 2);

        tree->decrement_num_nodes();

        REQUIRE(tree->num_nodes() == 1);
    }

    SECTION("Update minimum objective") {

        double min0 = tree->min_objective();
        double min1 = min0 + 0.01;

        tree->update_min_objective(min1);

        REQUIRE(tree->min_objective() == min1);
    }

    /** TODO: Check if the expected behavior of prune up is this **/
    SECTION("Prune up") {

        Node * n = root;
        int depth = 3;

        for(int i = 0; i < depth; i++) {
            n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
            tree->insert(n);
        }

        REQUIRE(tree->num_nodes() == (depth + 1));
        REQUIRE(n->depth() == depth);

        tree->prune_up(n);

        CHECK_FALSE(tree->root() == NULL);
        CHECK(tree->num_nodes() == 1);
    }

    SECTION("Check prefix") {

        Node * n = root;
        int depth = 3;

        tracking_vector<unsigned short, DataStruct::Tree> prefix;

        for(int i = 0; i < depth; i++) {
            n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
            tree->insert(n);
            prefix.push_back(i+1);
        }

        REQUIRE(tree->num_nodes() == (depth + 1));
        REQUIRE(n->depth() == depth);

        CHECK(tree->check_prefix(prefix) == n);

        prefix[depth - 1] += 1;
        CHECK(tree->check_prefix(prefix) == NULL);

        n->parent()->delete_child(prefix[depth - 1]);
        CHECK(tree->check_prefix(prefix) == NULL);
    }

    SECTION("Delete subtree") {

        Node * n = root;
        int depth = 3;

        tracking_vector<unsigned short, DataStruct::Tree> prefix;

        for(int i = 0; i < depth; i++) {
            Node * n1 = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
            Node * n2 = tree->construct_node(i+2, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
            tree->insert(n1);
            tree->insert(n2);

            n = n1;

            prefix.push_back(i+1);
        }

        REQUIRE(tree->num_nodes() == (2 * depth + 1));
        REQUIRE(n->depth() == depth);

        Node * t = root->child(1);
        REQUIRE_FALSE(t == NULL);

        REQUIRE(tree->check_prefix(prefix) == n);

        delete_subtree(tree, t, false, false);

        CHECK(n->deleted());
        CHECK(tree->check_prefix(prefix) == NULL);
        // TODO: Check if num_nodes should actually be 2
        CHECK(tree->num_nodes() == 2);

        delete_subtree(tree, n, true, false);

        CHECK(tree->num_nodes() == 1);
    }

    SECTION("Update optimal rulelist") {

        tracking_vector<unsigned short, DataStruct::Tree> rule_list = {0, 2, 1, 3};
        unsigned short new_rule = 5;
        tree->update_opt_rulelist(rule_list, new_rule);

        rule_list.push_back(new_rule);

        REQUIRE(tree->opt_rulelist() == rule_list);
    }


    SECTION("Update optimal predictions") {

        tracking_vector<bool, DataStruct::Tree> predictions = {false, true, false};
        bool new_pred = false;
        bool new_default_pred = true;

        Node * n = root;
        int depth = predictions.size();

        for(int i = 0; i < depth; i++) {
            n = tree->construct_node(i+1, nrules, predictions[i], true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
            tree->insert(n);
        }

        REQUIRE(tree->num_nodes() == (depth + 1));
        REQUIRE(n->depth() == depth);

        tree->update_opt_predictions(n, new_pred, new_default_pred);

        predictions.push_back(new_pred);
        predictions.push_back(new_default_pred);

        REQUIRE(tree->opt_predictions() == predictions);
    }

    if(tree)
        delete tree;
}

TEST_CASE("Test prefix permutation map", "[prefixmap]") {

    double c = 0.01;
    PrefixPermutationMap * pmap = new PrefixPermutationMap();
    REQUIRE_FALSE(pmap == NULL);

    CacheTree * tree = new CacheTree(nsamples, nrules, c, rules, labels, NULL, 0, false, "node");
    REQUIRE_FALSE(tree == NULL);

    tree->insert_root();

    REQUIRE_FALSE(tree->root() == NULL);

    /**
        In these tests, a canonical prefix of 1, 2, 4, 5
        is used, in three different permutations. Each
        permutation contains has three of its numbers
        in the parent_prefix, and the last as the added rule.
    **/

    bool prediction = true;
    bool default_prediction = true;
    double lower_bound = 0.1;
    double objective = 0.5;
    int len_prefix = 4;

    unsigned short correct_key[] = {4, 1, 2, 4, 5};

    tracking_vector<unsigned short, DataStruct::Tree> parent_prefix = {4, 2, 1};
    int new_rule = 5;
    unsigned char correct_indices[] = {4, 2, 1, 0, 3};

    // For second and third tests
    tracking_vector<unsigned short, DataStruct::Tree> parent_prefix_2 = {1, 4, 5};
    int new_rule_2 = 2;
    unsigned char correct_indices_2[] = {4, 0, 2, 3, 1};

    /** TEST 1 **/
    SECTION("Insert into empty map") {

        Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                                lower_bound, objective, tree->root(),
                                0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                parent_prefix);

        REQUIRE_FALSE(n == NULL);
        REQUIRE(pmap->getMap()->size() == 1);

        PrefixMap::iterator inserted = pmap->getMap()->begin();

        // Is inserted a valid pointer?
        REQUIRE_FALSE(inserted == pmap->getMap()->end());

        // Check if the lower bound was recorded correctly
        REQUIRE(inserted->second.first == lower_bound);

        unsigned short* key = inserted->first.key;
        unsigned char* indices = inserted->second.second;

        REQUIRE(key[0] == indices[0]);
        REQUIRE(key[0] == len_prefix);

        // Check if the inserted key and indices are correct
        for(int i = 0; i < len_prefix+1; i++) {
            CAPTURE(i);
            CHECK(key[i] == correct_key[i]);
            CHECK(indices[i] == correct_indices[i]);
        }

        // Check if the node was created correctly
        REQUIRE(n->parent() == tree->root());
        REQUIRE(n->prediction() == prediction);
        REQUIRE(n->default_prediction() == default_prediction);
        REQUIRE(n->lower_bound() == lower_bound);
        REQUIRE(n->objective() == objective);
    }

    /** TEST 2 **/
    SECTION("Insert with higher lower bound") {

        Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                                lower_bound, objective, tree->root(),
                                0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                parent_prefix);

        REQUIRE_FALSE(n == NULL);
        REQUIRE(pmap->getMap()->size() == 1);

        double h_bound = lower_bound + 0.02;

        // Expected behavior is that the map remains unchanged, since h_bound
        // is greated than lower_bound
        Node * n2 = pmap->insert(new_rule_2, nrules, prediction, default_prediction,
                                 h_bound, objective, tree->root(),
                                 0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                 parent_prefix_2);

        REQUIRE(pmap->getMap()->size() == 1);

        PrefixMap::iterator inserted = pmap->getMap()->begin();

        unsigned short* key = inserted->first.key;
        unsigned char* indices = inserted->second.second;

        REQUIRE(key[0] == indices[0]);
        REQUIRE(key[0] == len_prefix);

        // Check if the key and indices are unchanged (same as the ones inserted with n instead of n2)
        for(int i = 0; i < len_prefix+1; i++) {
            CAPTURE(i);
            CHECK(key[i] == correct_key[i]);
            CHECK(indices[i] == correct_indices[i]);
        }

        // Check if the node wasn't inserted (it should not have, since the permutation bound should block it)
        CHECK(n2 == NULL);

        // Check if the lower bound is unchanged
        CHECK(pmap->getMap()->begin()->second.first == lower_bound);
    }

    /** TEST 3 **/
    SECTION("Insert with lower lower bound") {

        Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                                lower_bound, objective, tree->root(),
                                0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                parent_prefix);

        REQUIRE_FALSE(n == NULL);
        REQUIRE(pmap->getMap()->size() == 1);

        double l_bound = lower_bound - 0.02;

        // Expected behavior is that the map will change the indices
        // and update the best permutation
        Node * n2 = pmap->insert(new_rule_2, nrules, prediction, default_prediction,
                                 l_bound, objective, tree->root(),
                                 0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                 parent_prefix_2);

        REQUIRE(pmap->getMap()->size() == 1);

        PrefixMap::iterator inserted = pmap->getMap()->begin();

        unsigned short* key = inserted->first.key;
        unsigned char* indices = inserted->second.second;

        REQUIRE(key[0] == indices[0]);
        REQUIRE(key[0] == len_prefix);

        // Check if the indices are changed and are correct (new values)
        for(int i = 0; i < len_prefix+1; i++) {
            CAPTURE(i);
            CHECK(key[i] == correct_key[i]);
            CHECK(indices[i] == correct_indices_2[i]);
        }

        // Check if the node was inserted
        CHECK_FALSE(n2 == NULL);

        // Check if the lower bound is the new correct lower bound
        CHECK(pmap->getMap()->begin()->second.first == l_bound);
    }

    if(pmap)
        delete pmap;

    if(tree)
        delete tree;
}

TEST_CASE("Test queue", "[queue]") {

    Queue * queue = new Queue(lb_cmp, "LOWER BOUND");
    REQUIRE_FALSE(queue == NULL);
    CHECK(std::string(queue->type()) == "LOWER BOUND");

    CacheTree * tree = new CacheTree(nsamples, nrules, 0.01, rules, labels, NULL, 0, false, "node");
    REQUIRE_FALSE(tree == NULL);

    tree->insert_root();
    REQUIRE_FALSE(tree->root() == NULL);

    SECTION("Push and Front") {
        queue->push(tree->root());

        REQUIRE_FALSE(queue->empty());
        REQUIRE(queue->size() == 1);
        REQUIRE(queue->front() == tree->root());
    }

    SECTION("Pop") {
        queue->push(tree->root());
        REQUIRE(queue->size() == 1);

        queue->pop();
        REQUIRE(queue->empty());
        REQUIRE(queue->size() == 0);
    }

    // TODO: Chcek select function

    if(queue)
        delete queue;

    if(tree)
        delete tree;
}
