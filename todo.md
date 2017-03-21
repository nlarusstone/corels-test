# To do

## Code review notes on ([clean-up branch](https://github.com/elaine84/bbcache/blob/clean-up/todo.md))

## Short paper (and by extension, long paper)

- [ ] Add a sentence for Rudin and Ertekin's work (Cynthia)
- [ ] Check language regarding best-first search, priority queue and metric
- [ ] Clarify that our experiments with the priority queue use the lower bound
- [ ] Delete references (in the intro and implementation) to things we haven't done or don't evaluate?
- [ ] Make room for and add acknowledgements
- [ ] Provide github link for our code
- [ ] Revisit Johann's comments (Elaine)
- [ ] Add C4.5 to stop-and-frisk with broken axis (Elaine)
- [ ] Try to make RIPPER work on stop-and-frisk (Elaine)
- [x] Add runtime to Fig 6 subfigures (vertical line) and update caption (Elaine)

## Long paper

- [ ] See http://www.jmlr.org/format/format.html (Everyone)
- [ ] Fill in acknowledgements (Everyone)
- [x] Add paragraphs on Hongyu's and Ertekin's papers in related work (Cynthia)
- [ ] Extended version of our short paper's implementation section (Nicholas)
- [ ] Add measurements, and update the writing if relevant (Nicholas)
- [ ] Add a more detailed description of our algorithm as pseudocode, that includes all bounds and data structures (Nicholas)
- [ ] Flag new paragraphs for others (Elaine)
- [x] Add clarification around the similarity bound that we aren't yet using it, possible future work (Elaine)
- [x] Add proofs for equivalent points bounds (Elaine)
- [x] Convert to JMLR format (Elaine)
- [ ] Add sentences in experiments section about how the order of the bounds matters (Elaine)
- [ ] Note that ablation results / efficacy of different CORELS components are heavily dataset-dependent (Elaine)
- [ ] More description about stop-and-frisk problem and dataset and describe the problems with bullet points (Elaine)
- [x] Add details about algorithm implementations and parameters used (Elaine)
- [ ] Emphasize the intuitive interpretation of our objective function, including the regularization parameter (Elaine)
- [ ] Provide more examples of rule lists that we find (Elaine)
- [ ] Ablation experiment for a dataset where the equivalent points bound doesn't help (e.g., tic-tac-toe)
- [ ] Show improvements due to curiosity on tic-tac-toe, and ideally something else (Elaine)
- [ ] Add section on curiosity -- this depends on showing results (Elaine)

-----

## Long paper (wish list post-submission)

### Definitions

- [ ] Stop overloading the notation for misclassification error (takes 3 arguments always)
- [ ] Swap the arguments in the notation for captures

### Data

- [ ] Of those stopped, who is frisked (or searched)?
- [ ] Maybe something about hospital readmissions
- [ ] Kaggle had a maybe interesting housing dataset
- [ ] Look at the datasets from Stat 220
- [ ] Figure out what is going on with the nursery dataset -- maybe ping Hongyu again (Elaine)

### Implementation

- [ ] Add BitVector node and a version of our algorithm (probably using new functions) that uses it (`captured_vector` branch)

### Experiments

- [ ] Measurements with and without our symmetry map using captured bit vectors
- [ ] Should we output confusion matrices?
- [ ] Add results for adult, with one and two clauses (Elaine)
- [ ] Describe the logger

### Logger analysis: Timing measurements (see Elaine email 3/6)

- [ ] Add a timing measurement around `garbage_collect(.)` and check the above assertion.
- [ ] Modify `logger.setLowerBoundTime(time_diff(t1))` to report cumulative time measurements,
      analogous to `logger.addToObjTime(time_diff(t2))`
- [ ] Add a timing measurement for the identical points bound.
- [ ] Complete the analysis of our timing measurements -- update the figure and generate a table summary.

### Logger analysis: Operations and data structures (see Elaine email 3/7)

- [ ] Separately measure the effects of our two support bounds (low priority).
- [ ] Summarize our results in 1-2 tables.

### Logger analysis: Other

- [ ] Revisit the remaining logger fields

### General

- [ ] Do we want a more thorough description of how we do rule mining, and our bit vector representation and operations?
- [ ] Subsets of data

-----

**Stuff below hasn't been organized recently, but contains some useful thoughts and notes**

## bbound improvements

- [ ] Add stopping condition based on the number of iterations

- [ ] Add policy that switches from curiosity to BFS

- [ ] Measure our logging overhead and determine a useful heuristic threshold
      (e.g., "writing a log entry every 50 iterations incurs about 1% overhead on tdata")

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

- [ ] The above bound seems to incur about a 10% overhead (in time),
      so add an option to switch this off and instead use the coarse-grain bound (Elaine)

- [ ] Calculate above bound in a separate process

- [ ] Properly calculate log10 of the remaining search space --
      see `getLogRemainingSpaceSize()` in `utils.hh` --
      you'll probably need to either write your own function or switch from `mpz` to `mpfr`

## Framework for experiments and analysis

- [ ] Analyze our timing measurements -- where does our algorithm spend its time?
      Does this change during execution?  See `eval/scratch.py` for preliminary analysis.

## Algorithms and data structures

A place to note things we haven't implemented, but might

- [ ] Anything we forgot about from our original Python implementation?
- [ ] Framework to remember rejected antecedents
- [ ] Framework aware of rules that commute
- [ ] Framework aware of dominates relationships
- [ ] Ability to switch between scheduling policies
- [ ] Something like Thompson sampling using curiosity
- [ ] Priority metric that blends between breadth-first and curiosity (non-stochastic)
- [ ] Enforce that the output optimal rule list is the simplest
- [ ] Explore simplifying constraints, e.g., rule lists whose predictions (never or rarely) switch between classes
- [ ] A framework for leveraging our similar support bound (via locality-sensitive hashing?)
- [ ] Parallelism :)
