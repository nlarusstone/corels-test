# Verbosity

## Areas where debug messages are printed:

`main.cc:136`: Operating system info

    if (verbosity >= 10)
        print_machine_info();

`main.cc:142`: "Writing optimal rule list to..." (works in bbcache but not in main repo)

This always gets printed regardless of verbosity level. We should have an option (on by default in CMD but not on Web UI) for this.

    snprintf(froot, BUFSZ, "../logs/for-%s-%s%s-%s-%s-removed=%s-max_num_nodes=%d-c=%.7f-v=%d-f=%d",
            pch ? pch + 1 : "",
            run_bfs ? "bfs" : "",
            run_curiosity ? curiosity_map[curiosity_policy].c_str() : "",
            use_prefix_perm_map ? "with_prefix_perm_map" :
                (use_captured_sym_map ? "with_captured_symmetry_map" : "no_pmap"),
            meta ? "minor" : "no_minor",
            ablation ? ((ablation == 1) ? "support" : "lookahead") : "none",
            max_num_nodes, c, verbosity, freq);

`main.cc:154`: Print rules and labels; break this up into one parameter for actual rules and other for bit vector samples

    if (verbosity >= 1000) {
        printf("\n%d rules %d samples\n\n", nrules, nsamples);
        rule_print_all(rules, nrules, nsamples);

        printf("\nLabels (%d) for %d samples\n\n", nlabels, nsamples);
        rule_print_all(labels, nlabels, nsamples);
    }

`main.cc: 162`: logger creation; enable dumping to log file if verbosity > 1 (otherwise only dump ORL at end)

    if (verbosity > 1)
        logger = new Logger(c, nrules, verbosity, log_fname, freq);
    else
        logger = new NullLogger();

`corels.cc:200`: garbage collection debug info

    if (verbosity >= 10)
        printf("before garbage_collect. num_nodes: %zu, log10(remaining): %zu\n",
                tree->num_nodes(), logger->getLogRemainingSpaceSize());

`corels.cc:206`: garbage collection debug info

    if (verbosity >= 10)
        printf("after garbage_collect. num_nodes: %zu, log10(remaining): %zu\n", tree->num_nodes(), logger->getLogRemainingSpaceSize());

`corels.cc:218`: if iterated 10k times, print metrics

    if (verbosity >= 10)
        printf("iter: %zu, tree: %zu, queue: %zu, pmap: %zu, log10(remaining): %zu, time elapsed: %f\n",
                num_iter, tree->num_nodes(), q->size(), p->size(), logger->getLogRemainingSpaceSize(), time_diff(start));

`corels.cc:228`: final metrics printing

    if (verbosity >= 1)
        printf("iter: %zu, tree: %zu, queue: %zu, pmap: %zu, log10(remaining): %zu, time elapsed: %f\n",
                num_iter, tree->num_nodes(), q->size(), p->size(), logger->getLogRemainingSpaceSize(), time_diff(start));

Verbosity flags:

* rule
* label
* samples
* progress
* log

i.e. `--verbosity=rule,label,progress`

Default should be `--verbosity=progress`

Indicate "WARNING: LONG" on UI for samples option

If debug is enabled, allow user to download or view log file
