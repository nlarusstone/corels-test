#include "rule.h"

#define CATCH_CONFIG_RUNNER
#include "catch.hpp"

rule_t * rules;
rule_t * labels;
int nrules;
int nsamples;

int main(int argc, char* argv[])
{
    rules = NULL;
    labels = NULL;

    int r = rules_init("./tests.out", &nrules, &nsamples, &rules, 1);
    int l = rules_init("./tests.label", &nlabels, &nsamples_chk, &labels, 0);

    if(r != 0 || l != 0 || nsamples != nsamples_chk)
    {
        printf("ERROR: Could not load rules or samples\n");
        return 1;
    }

    return 0;
}
