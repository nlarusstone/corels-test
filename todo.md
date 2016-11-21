Misc.
=====

- [ ] Find a cool dataset (Cynthia?)
- [ ] Change the default regularization parameter to c = 0.01
- [ ] Write out wall clock timestamps, including final total time, to stdout messages
- [ ] Write out rule list accuracy (in addition to objective value)
- [ ] Write out human-readable representation of optimal rule list
- [ ] Bonus: Write out tex representation of optimal rule list (see Fig. 1 in paper)
- [ ] Add a parameter to control the frequency of writing log records
- [ ] Measure our logging overhead and determine a useful heuristic threshold
      (e.g., "writing a log entry every 50 iterations incurs about 1% overhead on tdata")
- [ ] Bonus: In addition to the machine-readable log file, write out a human-readable
      report file (e.g., more or less what we're writing to stdout, potentially
      with some additional metadata, such as information about the machine used to
      run the experiment)
- [ ] Implement a way to downsample an input dataset and add a parameter for this

Rule mining
===========

- [ ] Investigate whether there's a problem with how we're using Ben's rule mining code.
      Elaine wrote `code/ben.py`, which modifies `BRL_code.py` from Cynthia's website.
      The `small()` function at the end of `ben.py` is used to generate the small datasets.
      The issue is that we seem to get some duplicate rules (e.g., a rule of the form
      `A AND B` as well as `B AND A`) -- e.g., I think that `data/bcancer.out` has this
      problem.  Figure out what the issue is and/or filter the rules to remove duplicates,
      before the output file is created.

- [ ] Next, fix the small dataset files (x.out, x = bcancer, cars, haberman, monks1, monks2, monks3, votes)
      by running `small(din='../data/small', dout='../data', maxlhs=2, minsupport=1)`.
      Check these new files into the repo.  Below, note the number of mined rules for each dataset.

- [ ] Also fix the telco file.  Make sure to use `maxlhs=2` and `minsupport=1`.

Framework for experiments and analysis
======================================

Note that Elaine made some drafts of figures in `eval/scratch.py` 

- [ ] Set up scripts to help run and manage experiments (probably bash and/or Python), and automatically analyze logs
- [ ] Map out what you think belongs in the ablation experiment
- [ ] Bonus: Write a framework (script?) for running an ablation experiment, and try it out on tdata

bbound experiments
==================

In our work in Python over the summer, we found that we could complete
some experiments in a reasonable amount of time but not others.
It would be valuable to try rerunning these experiments to see what happens.
Note the command run, approximate total time and machine used to run each experiment.

* tdata_R

- [x] tdata_R with c = 0.001, curiosity, permutation map (< 10 s on Elaine's home MacBook Pro)

    `./bbcache -c -p 1 -r 0.001 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.01, curiosity, permutation map (~ 10 min on Elaine's home MacBook Pro)

    `./bbcache -c -p 1 -r 0.01 -n 1000000 ../data/tdata_R.out ../data/tdata_R.label`

- [ ] tdata_R with c = 0.001, breadth-first, permutation map (might need lots of memory)
- [ ] tdata_R with c = 0.001, curiosity (might be unreasonable or need lots of memory)
- [ ] tdata_R with c = 0.001, breadth-first (might be unreasonable)

* small datasets:  bcancer, cars, haberman, monks1, monks2, monks3, votes

**See the rule mining section above first!**

- [ ] c = 0.02, curiosity, permutation map (all should finish in a reasonable amount of time)
- [ ] c = 0.01, curiosity, permutation map (monks1, monks3, votes should all complete,
      but we haven't seen any of bcancer, cars, haberman, monks2 complete)

* adult

- [ ] Downsample to ~10% of the data, and try c = 0.01, curiosity, permutation map.
      If that looks like it's taking forever, try c = 0.02 (I think that will work)
      and then 0.019, 0.018, etc.

* telco

**See the rule mining section above first!**

- [ ] Try c = 0.01, curiosity, permutation map.

Other experiments
=================

- [ ] Figure out how to use competing algorithms (see notes in paper)

Writing
=======

- [ ] Abstract
- [ ] Intro
- [ ] Related work: summarize Ben's and Hongyu's papers and describe how our work
      relates, builds on, and differs from their recent work (1 paragraph) -- remember
      that we're using the same rule mining approach as both as well as the rule library
- [ ] Related work: summarize the Garofalakis papers (1 paragraph)
- [ ] Related work: everything else (Cynthia?)
- [ ] Incremental branch-and-bound computation (Elaine)
- [ ] Rule mining: see Ben's paper (1 paragraph)
- [ ] Bit vector operations and rule library: see Hongyu's paper (1 paragraph,
      a new section before or after rule mining section?) -- we use a handful of
      operations, which ones and why?  (Why not others?)
- [ ] 
- [ ] Pseudocode closer to the algorithms we actually implement (Elaine)
- [ ] Elaine will flesh out the outline of Section 5 better so everyone can help fill it in

Algorithms
==========

A place to note things we haven't implemented, but might

- [ ] Framework to remember rejected antecedents
- [ ] 