/***  MAIN FILE WITH THE ACTUAL TESTS ***/

#define PREFIX_MAP_TESTS
#include "../queue.hh"

#include "catch.hpp"

extern rule_t * rules;
extern rule_t * labels;
extern int nrules;
extern int nsamples;

TEST_CASE("Test prefix permutation map", "[prefixmap]") {

    double c = 0.01;
    PrefixPermutationMap * pmap = new PrefixPermutationMap();
    CacheTree * tree = new CacheTree(nsamples, nrules, c, rules, labels, NULL, 0, false, "node");

    REQUIRE_FALSE(pmap == NULL);
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

    Queue * queue = new Queue(lb_cmp, )
}

TEST_CASE("Test trie", "[trie]") {
    double c = 0.01;
    CacheTree * tree = new CacheTree(nsamples, nrules, c, rules, labels, NULL, 0, false, "node");

    REQUIRE_FALSE(tree == NULL);

    SECTION("Insert root") {

        tree->insert_root();
        Node * r = tree->root();

        REQUIRE_FALSE(r == NULL);
    }

    if(tree)
        delete tree;
}
