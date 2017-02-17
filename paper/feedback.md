# From Daniel

## Abstract
It should be sharper. It's not clear why our method is a good alternative to CART, etc. We just say it is
an alternative. We should stress that CORELS is just (or at least in most cases) as accurate as
other decision tree methods but more importantly our model size is much smaller because of our exploration method
(thus making our solutions more interpretable?).

## Intro
~~"custom curiosity function" -- we don't define nor use this anywhere in the paper.~~

*Now "a priority queue whose priority metric is customizable,"*

## Section 3.1

In the example in equation 2, did you mean to put
cap(x_n, {p_k} | d_p) since you say that \beta should be a set?

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

Also, the end of that paragraph ends with a run-on sentence and should probably be split into 2 sentences.

pp4: we mention we provide a collection of near-optimal solutions and the distance between each such solution -- we currently don't do that (though we could) and we never mention these near-optimal solutions again.

Also, did we agree we wanted to say certificate?

## p2

pp1: "each path in the tree represents a rule list with the final node in the path.." -> "each path in the tree represents a rule list such that the final node in the path.."

pp2: we use the word proprietary (which I know is part of the reason Cynthia hates COMPAS), but I think we really mean non-interpretable/black box

## p3

pp1: we have a sentence "Figure 1 illustrates a rule list." -- Could we just use (Fig 1.) after the previous sentence (or is that just for bio papers).

The paragraph on capturing data: "Now let d_p be an ordered list of antecedents..." is fairly confusing, even for me

Should the paragraph right before 3.2 be there? Seems a little out of place.

## p4
The description of Algorithm 1 says "Branch-and-bound" but we used "Branch-and-cut" earlier

~~The footnote mentions a long version of this report without saying where it is~~

*Now added "(in preparation)" for both such footnotes*

## p5
~~Theres a (??) near the bottom of the right column -- and I'm not sure what it's referring to.~~

*Now refers to 3.1*

## p6
We say "permutation-aware garbage collection" at the bottom of the left column even though we refer to it as "symmetry-aware garbage collection" in the rest of the paper.

## p7
~~Bottom of left column: we refer to a trie, a symmetry-aware map... -- do we want to call it a prefix-trie?~~

*Now says "trie (prefix tree)" the first time it's mentioned*

pp "Mapping our algorithm": we mention checking that the lower bound is less than the minimum objective -- should we mention that we check all of the bounds we just proved above?
There seems to be a lot of whitespace above section 5 Experiments

## p8
I printed in black and white and some of the differences in the figures can be hard to see (I don't know if this is a case we care about).
