/** HELPER FILE FOR TESTS.CC ***/

#include "../rule.h"
#include "../utils.hh"

#define CATCH_CONFIG_RUNNER
#include "catch.hpp"

rule_t * rules;
rule_t * labels;
int nrules;
int nsamples;

NullLogger * logger;

int main(int argc, char* argv[])
{
    rules = NULL;
    labels = NULL;

    int nlabels, nsamples_chk;

    logger = new NullLogger();

    if(!logger)
    {
        printf("ERROR: Coult not create logger\n");
        return 1;
    }

    int r = rules_init("testing/tests.out", &nrules, &nsamples, &rules, 1);
    int l = rules_init("testing/tests.label", &nlabels, &nsamples_chk, &labels, 0);

    if(r != 0 || l != 0 || nsamples != nsamples_chk)
    {
        printf("ERROR: Could not load rules or samples\n");
        delete logger;
        return 1;
    }

    int ret = Catch::Session().run(argc, argv);

    rules_free(rules, nrules, 1);
    rules_free(labels, nlabels, 0);

    delete logger;

    return (ret < 0xff ? ret : 0xff);
}
