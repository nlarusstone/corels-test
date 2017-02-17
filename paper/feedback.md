# From Daniel

## Abstract
It should be sharper. It's not clear why our method is a good alternative to CART, etc. We just say it is
an alternative. We should stress that CORELS is just (or at least in most cases) as accurate as
other decision tree methods but more importantly our model size is much smaller because of our exploration method
(thus making our solutions more interpretable?).

*I would say that CART is competitive on both accuracy and model size (and RIPPER, at least for COMPAS). That we can certify optimality is what really distinguishes us for the examples we show in the experiments section.*

## Intro
~~"custom curiosity function" -- we don't define nor use this anywhere in the paper.~~

*Now "a priority queue whose priority metric is customizable,"*

## Section 3.1

In the example in equation 2, did you mean to put
cap(x_n, {p_k} | d_p) since you say that \beta should be a set?

*p_k on the left is a single antecedent -- is this what's confusing?*

Why not supp(x, \beta) (for definition notational consistency sake) and not supp(\beta, x)?
This is not a big deal though. But supp(\beta, x) is defined in terms of cap(x_n, \beta).

*I know... A hole I dug myself into a long time ago.  I didn't define macros and don't want to fix it everywhere.  These choices had been motivated by the phrases along the lines of "data captured by a prefix" and "a prefix's support for some dataset".  I actually probably prefer cap(\beta, x_n) because elsewhere I tend to list x and y last (e.g., in the objective and loss functions).  If you'd like to fix this by creating a macro, please do!  While you're at it, another thing to fix would be to make the loss function notation consistent.  l(d, x, y) means that l_0(d_p, \delta_p, x, y) should be l_0((d_p, \delta_p), x, y) and same thing for lp(.)*

## Section 3.7

~~5. Page 5: missing section reference?
"...we can furthermore apply it in the context of rule mining (§??).
Specifically, it implies that we should only mine rules with normalized..."~~

*Now refers to 3.1*

## Experiments

~~We say "We first ran a 10-fold cross-validation experiment using CORELS and eight other algorithms..."
But our figures only show results against C4.5, CART, RIPPER, and SBRL. Maybe we should stress that figure 2,3 only
shows numbers for methods for which we can determine a (straightforward and comparable) model size?~~

*Now there's a paragraph: "Figure 2 summarizes differences in accuracy and model size
for CORELS and other tree (CART, C4.5) and rule list (RIPPER, SBRL) learning algorithms.
Here, we also show results using a 2014 stop-and-frisk dataset from the
New York Civil Liberties Union (NYCLU)~\cite{nyclu:2014}, for predicting whether
a weapon will be found on a stopped individual who is frisked or searched."*

# From Nicholas

## p1

~~pp2: we list the same 3 references for two sentences in a row (3, 29, 30) -- maybe we should deduplicate this?~~

*Now refs appear once and sentences joined via semicolon*

~~pp3: we mention the ProPublica article and then Larson et al. without connecting the two -- do we expect readers to look in our references each time we make a reference?~~

*Now: "Consider the recent ProPublica article on the COMPAS recidivism prediction tool~\citep{LarsonMaKiAn16}. It highlights a case where a black-box, proprietary predictive model is being used for recidivism prediction. The authors show that the COMPAS scores are racially biased, but since the model is not transparent, no one (outside of the creators of COMPAS) can determine the reason or extent of the bias~\citep{LarsonMaKiAn16}"*

~~Also, the end of that paragraph ends with a run-on sentence and should probably be split into 2 sentences.~~

*The last sentence or the last two?  I've slightly rewritten the last two as three: "Answering that question requires solving a computationally hard problem. Namely, we would like to find a transparent model that is optimal within a particular pre-determined class of models, and produce a certificate of optimality. This would enable one to say, for this problem and model class, with certainty and before resorting to black box methods, whether there exists a transparent model."*

pp4: we mention we provide a collection of near-optimal solutions and the distance between each such solution -- we currently don't do that (though we could) and we never mention these near-optimal solutions again.

*I've tempered this by inserting "optionally," -- is this toned down enough?*

~~Also, did we agree we wanted to say certificate?~~

*I'm ok with "certificate," which Cynthia uses a few other times in the intro*

## p2

~~pp1: "each path in the tree represents a rule list with the final node in the path.." -> "each path in the tree represents a rule list such that the final node in the path.."~~

*Done*

~~pp2: we use the word proprietary (which I know is part of the reason Cynthia hates COMPAS), but I think we really mean non-interpretable/black box~~

*I've added "black box"*

## p3

~~pp1: we have a sentence "Figure 1 illustrates a rule list." -- Could we just use (Fig 1.) after the previous sentence (or is that just for bio papers).~~

*We could but I tend to go with the more verbose style.*

The paragraph on capturing data: "Now let d_p be an ordered list of antecedents..." is fairly confusing, even for me

*I agree!  Any suggestions?*

~~Should the paragraph right before 3.2 be there? Seems a little out of place.~~

*Less awkward, I hope: "Finally, we note that our approach leverages pre-mined rules,
following the methodology taken by~\citet{LethamRuMcMa15} and~\citet{YangRuSe16}.
One of the results we prove later implies a constraint
that can be used as a filter during rule mining --
they must have at least some minimum support
given by the lower bound in Theorem~\ref{thm:min-capture}."*

## p4
The description of Algorithm 1 says "Branch-and-bound" but we used "Branch-and-cut" earlier

*Indeed, and we mention branch-and-bound more than once.  I asked Cynthia at some point if we can
say branch-and-bound and it's fine (just not something we wanted to emphasize, e.g., in the title).
I could imagine only using "branch-and-bound"...*

I would tend to prefer just using "branch-and-bound" unless there's a particular reason we say "branch-and-cut" in the following: 'and in particular, a special branch- and-cut algorithm, called Certi ably Optimal RulE ListS (CORELS).'

~~The footnote mentions a long version of this report without saying where it is~~

*Now added "(in preparation)" for both such footnotes*

## p5
~~Theres a (??) near the bottom of the right column -- and I'm not sure what it's referring to.~~

*Now refers to 3.1*

## p6
We say "permutation-aware garbage collection" at the bottom of the left column even though we refer to it as "symmetry-aware garbage collection" in the rest of the paper.

*We actually also say "permutation-aware garbage collection" in the next column on the right (Section 3.8.2).  We say "symmetry-aware map" in the implementation and also now the experiments section (where it used to say permutation map).*

## p7
~~Bottom of left column: we refer to a trie, a symmetry-aware map... -- do we want to call it a prefix-trie?~~

*Now says "trie (prefix tree)" the first time it's mentioned*

pp "Mapping our algorithm": we mention checking that the lower bound is less than the minimum objective -- should we mention that we check all of the bounds we just proved above?

*Good point! I've added this sentence: "We also leverage our other bounds from Section 3
to aggressively prune the search space."*

~~There seems to be a lot of whitespace above section 5 Experiments~~

*I've added negative whitespace via \vspace{-1mm}.  Also I think this has reduced due to other edits that have happened.*

## p8
I printed in black and white and some of the differences in the figures can be hard to see (I don't know if this is a case we care about).

*I do care! Which ones have issues?*

Mainly in Fig. 3 (acc vs sparsity) the different techniques blend together because the shapes can be hard to distinguish. Also in Fig 5. the queue composition is really hard to tell apart because they're just different shades of gray.

*In Fig. 3 the markers are bigger.  In Fig 5, I've eliminated the legend and label the lines explicitly, and I think reversing the colors helps but I haven't checked.*
