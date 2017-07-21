
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

    SECTION("Insert into empty map") {

        //pmap->insert(1, nrules, 1, 1, 0.1, 0.12, tree->root(), 2, 5, 0, 0.01, 0.0, tree, NULL, tracking_vector<unsigned short, DataStruct::Tree>{});
    }

    SECTION("Insert with lower lb") {
    }

    SECTION("Insert with high lb") {
    }

    if(pmap)
        delete pmap;

    if(tree)
        delete tree;
}
