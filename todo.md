# To do

Feel free to edit and please add any items or even sections that come to mind.
Claim items by adding your name, and check them off when complete :)

## datasets

- [ ] Look for a large (classification) dataset at [Kaggle](https://www.kaggle.com/datasets)

- [ ] Look for a large (classification) dataset at the
      [UCI repository](https://archive.ics.uci.edu/ml/datasets.html?format=&task=cla&att=&area=&numAtt=&numIns=&type=&sort=nameUp&view=table)

- [ ] Look at the datasets from Stat 220 (Elaine)

## bbound improvements

- [ ] Add stopping condition based on the number of iterations

- [ ] Add policy that switches from curiosity to BFS

- [ ] Queue elements are printed to `queue.txt` -- make this optional,
      consider an input file name and threshold for number of printed entries

- [x] `bbound_queue` currently exits at 20,000 iterations -- make this optional
      and take an input argument for this threshold (this is used in the preliminary
      implementation of a policy that switches from curiosity to curious lower bound)

- [x] Write out human-readable representation of optimal rule list

- [x] Bonus: Write out tex representation of optimal rule list (see Fig. 1 in paper)

- [x] Add a parameter to control the frequency of writing log records

- [ ] Measure our logging overhead and determine a useful heuristic threshold
      (e.g., "writing a log entry every 50 iterations incurs about 1% overhead on tdata")

- [x] Bonus: In addition to the machine-readable log file, write out a human-readable
      report file (e.g., more or less what we're writing to stdout, potentially
      with some additional metadata, such as information about the machine used to
      run the experiment)

- [ ] Make R/Python binding so it is easier to run experiments. (Daniel)
      Link to SBRL cran repo: https://github.com/cran/sbrl. We can follow this format.

- [ ] What else should we measure?  E.g., think about time spent deleting nodes
      from the cache, garbage collection triggered by a new best objective value,
      etc.

- [ ] Consolidate algorithm state in the logger object

- [ ] The lower bound check before the call to `evaluate_children` does NOT require
      a trie lookup in the special case of a curious queue ordered by lower bound,
      in which case it could be considerably faster -- maybe want to specialize `queue_select`?

- [ ] Garbage collect the permutation map of prefixes longer than the maximum prefix length

- [x] How many times do we look up an item in the hash map that is not in the tree --
      added to logger at `_state.pmap_null_num`

- [x] When we do look up an item, how many times do we end up discarding
      something we would have been unable to discard had we not done this --
      added to logger at `_state.pmap_discard_num`, counts number of lookups
      that trigger a discard operation, not the total number of deleted nodes

- [ ] If garbage collecting the cache and queue would reduce the size of the queue
      by at least some factor (e.g., 10%) then do so -- can't iterate over
      `std::priority_queue` so this would require a different data structure,
      e.g., a custom subclass

- [ ] Make permutation map garbage collection optional

- [x] Estimate the size (in memory) of the permutation map compared to the cache --
      compare experiments for a fixed `max_num_nodes` with and without the
      permutation map.  Should we consider an alphabetical tree?

- [ ] Estimate the size (in memory) of the queue -- should we try to eliminate it?
      The queue is especially annoying if it retains many prefixes marked as deleted
      and is difficult to garbage collect.  However, it seems small compared to the cache,
      e.g., consider the following policies (curious lower bound queue with permutation map
      vs. stochastic with no queue or permutation map vs. bfs queue without pmap) --
      not truly a fair comparison because the distributions of prefix lengths differ

      `./bbcache -c 2 -p 1 -r 0.001 -n 100000000 ../data/tdata_R.out ../data/tdata_R.label` (15 GB)

      `./bbcache -s -r 0.001 -n 22460425 ../data/tdata_R.out ../data/tdata_R.label` (4 GB)

      `./bbcache -b -p 0 -r 0.001 -n 22460425 ../data/tdata_R.out ../data/tdata_R.label` (4.2 GB)

- [ ] Eliminate curious lower bound queue by propagating lower bounds up the tree;
      select next prefix by traversing path to node with smallest lower bound
      (implement as a separate algorithm)

- [ ] Can we eliminate the BFS queue by implementing BFS via tree traversal?

- [ ] Implement back-off and test on adult dataset (Nicholas)

- [x] Implement (during execution) calculation for tighter bound on size of remaining search space (Elaine)

- [ ] The above bound seems to incur about a 10% overhead (in time),
      so add an option to switch this off and instead use the coarse-grain bound (Elaine)

- [ ] Calculate above bound in a separate process

- [ ] Properly calculate log10 of the remaining search space --
      see `getLogRemainingSpaceSize()` in `utils.hh` --
      you'll probably need to either write your own function or switch from `mpz` to `mpfr`

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
      Note: Elaine re-ran this with `minsupport=1`

## Rule mining

- [ ] Fix the telco file.  Make sure to use `maxlhs=2` and `minsupport=1`.

## Framework for experiments and analysis

Note that Elaine made some drafts of figures in `eval/scratch.py` -- she used
`tabular` where you might prefer to use `pandas`, and `matplotlib` where you
might prefer to use `seaborn` (which is built on top of `matplotlib`).  Feel
free to use whatever data analysis and visualization tools you prefer, including
Jupyter notebooks!

- [X] Set up a framework for doing 10-fold cross-validation -- keep in mind that
      we'll want to run the same, randomly generated 10 folds on both our algorithms
      and competing algorithms. (Nicholas)

- [X] Consider setting up a script that will run the 10 folds in parallel. (Nicholas)

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

## Experiments

- [x] Figure out how to use code from Cynthia's students

- [x] Identify software packages for competing algorithms (see notes in paper):
      I think Daniel has done some work on this front?  Please take some notes
      here about what looks promising.

- [ ] Figure out how to use these algorithms and write useful scripts for
      running experiments.  If I understand correctly, we want to use datasets
      from before we do rule mining, e.g., see the files in `data/small/`. (Daniel)

- [ ] Generate Figure 2, which compares objective values and runtimes of different methods.
      Can do this as a draft on a small dataset, like tdata. (Daniel)

- [x] If we haven't yet handled 10-fold cross-validation, implement a framework for this!

## Writing

- [ ] Abstract

- [x] Intro -- look at Ben's and Hongyu's papers as examples.  Perhaps start by
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

- [X] Summarize Ben's and Hongyu's papers and describe how our work
      relates, builds on, and differs from their recent work (1 paragraph) -- remember
      that we're using the same rule mining approach as both as well as the rule library (Nicholas)

- [X] Summarize the Garofalakis papers (1 paragraph) (Nicholas)

- [x] Summarize the ProPublica paper (1 paragraph) (Nicholas)

- [ ] Everything else (Cynthia)

### Our approach

- [ ] Incremental branch-and-bound computation (Elaine)

- [ ] Rule mining: see Ben's paper (1 paragraph)

- [ ] Bit vector operations and rule library: see Hongyu's paper (1 paragraph,
      a new section before or after rule mining section?) -- we use a handful of
      operations, which ones and why?  (Why not others?)

- [ ] Pseudocode closer to the algorithms we actually implement (Elaine)

### Bounds

- [ ] Rewrite counting bounds with respect to Algorithm 2

### Implementation architecture

- [ ] Elaine will flesh out the outline of Section 5 better so everyone can help fill it in

### Evaluation

- [ ] Describe the physical computing environment used to conduct experiments (tbd)
- [ ] Describe and motivate the experiments we conduct
- [ ] Describe and interpret our results

### Other sections

- [ ] Conclusions and future work
- [ ] Acknowledgements -- everyone should ensure we're not missing anything or anyone here!

### Definitions (Elaine)

- [ ] Stop overloading the notation for misclassification error (takes 3 arguments always)
- [ ] Swap the arguments in the notation for captures

### Annoying tex things

- [ ] Figure out how to change the label of Algorithm 3 to something like Listing 3

## Algorithms and data structures

A place to note things we haven't implemented, but might

- [ ] Framework to remember rejected antecedents
- [ ] Framework aware of rules that commute
- [ ] Framework aware of dominates relationships
- [ ] Ability to switch between scheduling policies
- [x] Depth-first scheduling policy
- [ ] Something like Thompson sampling using curiosity
- [x] Different priority metrics: lower bound
- [x] Different priority metrics: objective
- [ ] Priority metric that blends between breadth-first and curiosity (non-stochastic)
- [ ] Enforce that the output optimal rule list is the simplest

## README, GNUmakefile, and dependencies

- [ ] Remove unnecessary dependencies from GNUmakefile (e.g., profiling tools)
- [ ] Update `readme.md` to explain all dependencies
