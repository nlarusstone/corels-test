/***  MAIN FILE WITH THE ACTUAL TESTS ***/

#define PREFIX_MAP_TESTS
#include "../pmap.hh"

#include "../alloc.hh"

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

    SECTION("Insert into empty map") {

        bool prediction = true;
        bool default_prediction = true;
        double lower_bound = 0.1;
        double objective = 0.5;
        int len_prefix = 3;

        /**
            In this test, a canonical prefix of 1, 2, 4
            is used, in three different permutations. For
            ecah permutation, a random new rule is added,
            and the behavior of the map is inspected.
        **/
        unsigned short correct_key[] = {3, 1, 2, 4};
        unsigned char correct_indices[] = {3, 2, 1, 0};
        unsigned char correct_new_indices[] = {3, 0, 2, 1};

        double l_bound = lower_bound - 0.02;
        double h_bound = lower_bound + 0.02;

        Node * n = pmap->insert(3, nrules, prediction, default_prediction,
                                lower_bound, objective, tree->root(),
                                0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                tracking_vector<unsigned short, DataStruct::Tree>{4,2,1});

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
        for(int i = 1; i < len_prefix+1; i++) {
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

        SECTION("Insert with higher lower bound") {

            // Expected behavior is that the map remains unchanged, since h_bound
            // is greated than lower_bound
            Node * n2 = pmap->insert(6, nrules, prediction, default_prediction,
                                     h_bound, objective, tree->root(),
                                     0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                     tracking_vector<unsigned short, DataStruct::Tree>{1,2,4});

            REQUIRE(pmap->getMap()->size() == 1);

            PrefixMap::iterator inserted_chk = pmap->getMap()->begin();

            unsigned short* key_chk = inserted_chk->first.key;
            unsigned char* indices_chk = inserted_chk->second.second;

            REQUIRE(key_chk[0] == indices_chk[0]);
            REQUIRE(key_chk[0] == len_prefix);

            // Check if the key and indices are the same as before
            for(int i = 1; i < len_prefix+1; i++) {
                CAPTURE(i);
                CHECK(key_chk[i] == correct_key[i]);
                CHECK(indices_chk[i] == correct_indices[i]);
            }

            // Check if the lower bound is unchanged
            CHECK(n2 == NULL);
            CHECK(pmap->getMap()->begin()->second.first == lower_bound);

            SECTION("Insert with lower lower bound") {

                // Expected behavior is that the map will change the indices
                // and update the best permutation of [1,2,4] to [1,4,2]
                Node * n3 = pmap->insert(5, nrules, prediction, default_prediction,
                                         l_bound, objective, tree->root(),
                                         0, nsamples, len_prefix, c, 0.0, tree, NULL,
                                         tracking_vector<unsigned short, DataStruct::Tree>{1,4,2});

                REQUIRE(pmap->getMap()->size() == 1);

                PrefixMap::iterator inserted_check = pmap->getMap()->begin();

                unsigned short* key_check = inserted_check->first.key;
                unsigned char* indices_check = inserted_check->second.second;

                REQUIRE(key_check[0] == indices_check[0]);
                REQUIRE(key_check[0] == len_prefix);

                // Check if the indices are changed and are correct (new values)
                for(int i = 1; i < len_prefix+1; i++) {
                    CAPTURE(i);
                    CHECK(key_check[i] == correct_key[i]);
                    CHECK(indices_check[i] == correct_new_indices[i]);
                }

                CHECK_FALSE(n3 == NULL);

                // Check if the lower bound is the new correct lower bound
                CHECK(pmap->getMap()->begin()->second.first == l_bound);
            }
        }
    }

    if(pmap)
        delete pmap;

    if(tree)
        delete tree;
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
