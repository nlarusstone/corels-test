# To do

Feel free to edit and please add any items or even sections that come to mind.
Claim items by adding your name, and check them off when complete :)

## bbound improvements

- [x] Change the default regularization parameter to c = 0.01

- [x] Write out wall clock timestamps, including final total time, to stdout messages

- [ ] Write out rule list accuracy (in addition to objective value) (Daniel)

- [x] Write out human-readable representation of optimal rule list

- [x] Bonus: Write out tex representation of optimal rule list (see Fig. 1 in paper)

- [x] Add a parameter to control the frequency of writing log records

- [ ] Measure our logging overhead and determine a useful heuristic threshold
      (e.g., "writing a log entry every 50 iterations incurs about 1% overhead on tdata")

- [x] Bonus: In addition to the machine-readable log file, write out a human-readable
      report file (e.g., more or less what we're writing to stdout, potentially
      with some additional metadata, such as information about the machine used to
      run the experiment)

- [ ] Implement a way to downsample an input dataset and add a parameter for this

- [ ] Can we answer Margo's questions about the effects of the permutation map?
      See the bulleted list at the start of the experiments section of the paper,
      and Margo and Elaine's emails from Nov 1.

- [ ] What else should we measure?  E.g., think about time spent deleting nodes
      from the cache, garbage collection triggered by a new best objective value,
      etc.

## ProPublica COMPAS dataset

- [x] Summarize the [ProPublica COMPAS dataset](https://github.com/propublica/compas-analysis).
      How many rows and columns?  Describe each column and report basic stats -- are the column
      values binary, categorical, integer, real, other?  Report mean, standard deviation,
      and ranges of numerical columns; categorical values, etc. (Nicholas)

- [x] Propose binary features and labels to extract, e.g., map categorical values to binary,
      identify meaningful ranges or threshold values for numerical columns, etc.
      (Nicholas will develop a preliminary design?
      We'll hopefully discuss this at our next meeting with Cynthia.)

- [x] Extract binary features and produce files for input into our algorithm. (Nicholas)

## Rule mining

- [x] Investigate whether there's a problem with how we're using Ben's rule mining code.
      Elaine wrote `code/ben.py`, which modifies `BRL_code.py` from Cynthia's website.
      The `small()` function at the end of `ben.py` is used to generate the small datasets.
      The issue is that we seem to get some duplicate rules (e.g., a rule of the form
      `A AND B` as well as `B AND A`) -- e.g., I think that `data/bcancer.out` has this
      problem.  Figure out what the issue is and/or filter the rules to remove duplicates,
      before the output file is created. (Nicholas)

- [ ] Next, fix the small dataset files (x.out, x = bcancer, cars, haberman, monks1, monks2, monks3, votes)
      by running `small(din='../data/small', dout='../data', maxlhs=2, minsupport=1)`.
      Check these new files into the repo.  Below, note the number of mined rules for each dataset.

- [ ] Also fix the telco file.  Make sure to use `maxlhs=2` and `minsupport=1`.

## Framework for experiments and analysis

Note that Elaine made some drafts of figures in `eval/scratch.py` -- she used
`tabular` where you might prefer to use `pandas`, and `matplotlib` where you
might prefer to use `seaborn` (which is built on top of `matplotlib`).  Feel
free to use whatever data analysis and visualization tools you prefer, including
Jupyter notebooks!

- [ ] Set up a framework for doing 10-fold cross-validation -- keep in mind that
      we'll want to run the same, randomly generated 10 folds on both our algorithms
      and competing algorithms.

- [ ] Set up scripts to help run and manage experiments (probably bash and/or Python),
      and automatically analyze logs

- [ ] Extend the analysis and visualization framework to report results across
      all 10 folds of cross-validation -- see Cynthia's sketches in `paper/figs/`.
      For many of the figures, we want to plot something like three trend lines
      corresponding to a mean and standard error.

- [ ] Map out what you think belongs in the ablation experiment

- [ ] Bonus: Write a framework (script?) for running an ablation experiment,
      and try it out on tdata

- [ ] Add analysis of timing measurements -- where does our algorithm spend its time?
      Does this change during execution?  See `eval/scratch.py` for preliminary analysis.

## bbound experiments

In our work in Python over the summer, we found that we could complete
some experiments in a reasonable amount of time but not others.  Now that
we have a C++ implementation that is more than an order of magnitude faster,
it would be valuable to try rerunning these experiments to see what happens.
Note the command run, approximate total time and machine used to run each experiment.

### tdata_R (Elaine)

On the tic-tac-toe dataset with `c = 0.001`, going from curiosity without the permutation
map to curiosity with the permutation map yields a speedup of > 100x :)

- [x] tdata_R with c = 0.001, curiosity, permutation map (< 10 s on Elaine's home MacBook Pro)

    `./bbcache -c -p 1 -r 0.001 -n 100000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.01, curiosity, permutation map (~ 10 min on Elaine's home MacBook Pro)

    `./bbcache -c -p 1 -r 0.01 -n 1000000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, breadth-first, permutation map

    Incomplete result: best has length 4 after ~ 9060 s (~ 150 min), ~ 375GB memory on beepbooop

    `./bbcache -b -p 1 -r 0.001 -n 1000000000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, curiosity (~ 1050 s on Elaine's home MacBook Pro; quickly finds optimal)

    `./bbcache -c -p 0 -r 0.001 -n 100000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, breadth-first (Elaine is declaring this unreasonable)

    `./bbcache -b -p 0 -r 0.001 ../data/tdata_R.out ../data/tdata_R.label`

### small datasets:  bcancer, cars, haberman, monks1, monks2, monks3, votes

**See the rule mining section above first!**

- [ ] c = 0.02, curiosity, permutation map (all should finish in a reasonable amount of time)

- [ ] c = 0.01, curiosity, permutation map (monks1, monks3, votes should all complete,
      but we haven't seen any of bcancer, cars, haberman, monks2 complete)

### adult

- [ ] Downsample to ~10% of the data, and try c = 0.01, curiosity, permutation map.
      If that looks like it's taking forever, try c = 0.02 (I think that will work)
      and then 0.019, 0.018, etc.

### telco

**See the rule mining section above first!**

- [ ] Try c = 0.01, curiosity, permutation map.

## Other experiments

- [ ] Find out if we can reuse code from any of Cynthia's students (Cynthia)

- [ ] Identify software packages for competing algorithms (see notes in paper):
      I think Daniel has done some work on this front?  Please take some notes
      here about what looks promising.

- [ ] Figure out how to use these algorithms and write useful scripts for
      running experiments.  If I understand correctly, we want to use datasets
      from before we do rule mining, e.g., see the files in `data/small/`.

- [ ] Generate Figure 2, which compares objective values and runtimes of different methods.
      Can do this as a draft on a small dataset, like tdata.

- [ ] If we haven't yet handled 10-fold cross-validation, implement a framework for this!

## Writing

- [ ] Abstract

- [ ] Intro -- look at Ben's and Hongyu's papers as examples.  Perhaps start by
      trying to tell a high-level story in approximately 10 sentences.
      (This might make a good abstract!)  When you flesh things out, the intro
      will probably be approximately one page.  Remember that our approach is
      motivated by human-interpretability.  Paint a landscape of previous
      approaches and where we fit in -- what makes our approach novel, and what
      are its unique advantages?  Arrive at a set of clear statements that
      highlight our main research contributions -- this can be done as a
      bulleted list.  What is our algorithmic approach?  What data structures
      do we leverage, and what do they achieve?  What theorems do we prove, and
      what are the algorithmic and practical consequences?  How do we implement
      and evaluate our algorithms? (Nicholas will write a draft, then Cynthia will take a pass)

### Related work

- [ ] Everyone should conduct a Google search on related work -- we might
      uncover new things we didn't know about. The related work sections in Ben's and Hongyu's
      papers provide good starting points.  If you find anything new that you think is
      important, add the bibtex info as well as a couple sentences describing the work.

- [ ] Summarize Ben's and Hongyu's papers and describe how our work
      relates, builds on, and differs from their recent work (1 paragraph) -- remember
      that we're using the same rule mining approach as both as well as the rule library

- [ ] Summarize the Garofalakis papers (1 paragraph)

- [ ] Everything else (Cynthia)

### Our approach

- [ ] Incremental branch-and-bound computation (Elaine)

- [ ] Rule mining: see Ben's paper (1 paragraph)

- [ ] Bit vector operations and rule library: see Hongyu's paper (1 paragraph,
      a new section before or after rule mining section?) -- we use a handful of
      operations, which ones and why?  (Why not others?)

- [ ] Pseudocode closer to the algorithms we actually implement (Elaine)

### Implementation architecture

- [ ] Elaine will flesh out the outline of Section 5 better so everyone can help fill it in

### Evaluation

- [ ] Describe the physical computing environment used to conduct experiments (tbd)
- [ ] Describe and motivate the experiments we conduct
- [ ] Describe and interpret our results

### Other sections

- [ ] Conclusions and future work
- [ ] Acknowledgements -- everyone should ensure we're not missing anything or anyone here!

## Algorithms and data structures

A place to note things we haven't implemented, but might

- [ ] Framework to remember rejected antecedents
- [ ] Framework aware of rules that commute
- [ ] Framework aware of dominates relationships
- [ ] Ability to switch between scheduling policies
- [ ] Depth-first scheduling policy
- [ ] Something like Thompson sampling using curiosity
- [ ] Different priority metrics: lower bound, objective
- [ ] Priority metric that blends between breadth-first and curiosity (non-stochastic)
- [ ] Enforce that the output optimal rule list is the simplest
