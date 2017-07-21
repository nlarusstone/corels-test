
#define PREFIX_MAP_TESTS
#include "../pmap.hh"

#include "../alloc.hh"

#include "catch.hpp"

extern rule_t * rules;
extern rule_t * labels;
extern int nrules;
extern int nsamples;

TEST_CASE("Test prefix permutation map", "[prefixmap]") {

    PrefixPermutationMap * pmap = new PrefixPermutationMap;
    CacheTree * tree = new CacheTree(nsamples, nrules, 0.01, rules, labels, NULL, 0, false, "node");

    REQUIRE_NOT(pmap == NULL);
    REQUIRE_NOT(tree == NULL);

    SECTION("Insert into empty map") {

        SECTION("Insert with lower lb") {

        }

        SECTION("Insert with high lb") {

        }
    }

    delete pmap;
    delete tree;
}
