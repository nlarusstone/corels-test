
#define PREFIX_MAP_TESTS
#include "../pmap.hh"

#include "../alloc.hh"

#include "catch.hpp"

extern rule_t * rules;
extern rule_t * labels;
extern int nrules;
extern int nsamples;

TEST_CASE("Test prefix permutation map", "[prefixmap]") {

    PrefixPermutationMap * pmap = new PrefixPermutationMap();
    CacheTree * tree = new CacheTree(nsamples, nrules, 0.01, rules, labels, NULL, 0, false, "node");

    REQUIRE_FALSE(pmap == NULL);
    REQUIRE_FALSE(tree == NULL);

    SECTION("Insert into empty map") {

        INFO("parent section");

        SECTION("Insert with lower lb") {
            INFO("first child section");
        }

        SECTION("Insert with high lb") {
            INFO("second child section");
        }
    }

    if(pmap)
        delete pmap;

    if(tree)
        delete tree;
}
