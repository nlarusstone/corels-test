# notes
A place to stash older notes, results, etc.

## serial_lazy.py

<!-- These are somewhat wrong
            warm=0.999  warm=0.99   warm=0.91   maximum
    len=0   1           1           1           1
    len=1   14          26          351         377
    len=2   171         592         97309       141752
    len=3   1856        12563       ?           53157000
    len=4   20061       259766      ?           19880718000
    len=5   243503      ?           ?           7415507814000

            warm=0.999  warm=0.99   warm=0.91   maximum
    len=0   1           1           1           1
    len=1   14          26          351         377
    len=2   x13         x23         x278        x376
    len=3   x11         x22         ?           x375
    len=4   x11         x21         ?           x374
    len=5   x12         ?           ?           x373
 -->

## serial_gc.py

### tdata with commuting

    froot = 'tdata_R'
    min_objective = 1.
    c = 0.
    max_prefix_length = 8
    garbage_collect = True

    cache size: [1, 14, 92, 416, 1746, 8431, 49474, 361820, 983133]
    dead prefix start: [0, 0, 0, 0, 0, 0, 0, 0, 0]
    caputed zero: [0, 0, 0, 0, 27, 478, 4743, 55155, 901311]
    stunted prefix: [0, 0, 0, 0, 0, 0, 0, 0, 0]
    commutes: [0, 0, 1366, 11025, 51660, 208056, 913480, 4870817, 32341564]
    dead prefix: [0, 363, 3791, 22925, 101220, 427543, 2111344, 12507000, 99515029]
    inferior: [0, 0, 15, 134, 931, 6750, 57291, 560062, 132363]
    seconds: [0.0, 0.0, 0.04, 0.18, 0.74, 3.06, 15.74, 104.71, 718.27]
    growth: [14.0, 6.57, 4.52, 4.2, 4.83, 5.87, 7.31, 2.72]

    if {c7=x,c8=x,c9=x} then predict 1
    else if {c1=x,c4=x,c7=x} then predict 1
    else if {c4=x,c5=x,c6=x} then predict 1
    else if {c1=x,c5=x,c9=x} then predict 1
    else if {c3=x,c6=x,c9=x} then predict 1
    else if {c3=x,c5=x,c7=x} then predict 1
    else if {c1=x,c2=x,c3=x} then predict 1
    else if {c2=x,c5=x,c8=x} then predict 1
    else predict 0

    prefix: (359, 64, 264, 73, 219, 211, 47, 147)
    prediction: (1, 1, 1, 1, 1, 1, 1, 1)
    accuracy: 1.0000000000
    upper_bound: 1.0000000000
    objective: 0.0000000000
    lower_bound: 0.0000000000
    num_captured: 408
    num_captured_correct: 408
    sum(not_captured): 231
    curiosity: 0.000

### tdata w/o commuting

    cache size: [1, 14, 92, 416, 1746, 8431, 49459, 361698, 520176]
    dead prefix start: [0, 0, 0, 0, 0, 0, 0, 0, 0]
    caputed zero: [0, 0, 13, 158, 1000, 6038, 36048, 261984, 2664696]
    stunted prefix: [0, 0, 0, 0, 0, 0, 0, 0, 0]
    dead prefix: [0, 363, 5081, 33343, 150098, 623799, 2950881, 16927278, 130609440]
    inferior: [0, 0, 78, 583, 2740, 12990, 99944, 798329, 33948]
    seconds: [0.0, 0.01, 0.04, 0.34, 1.3, 5.56, 20.83, 112.93, 702.97]

### tdata w/o garbage collection

    garbage_collect = False

    cache size: [1, 14, 170, 1842, 19890]
    seconds: [0.0, 0.02, 0.15, 2.07, 21.1]

    if {c3=o,c5=o,c7=o} then predict 0
    else if {c1=o,c5=o,c9=o} then predict 0
    else if {c3=o,c6=o,c9=o} then predict 0
    else if {c4=o,c5=o,c6=o} then predict 0
    else predict 1

### adult w/10% of dataset

    froot = 'adult_R'
    warm_start = True
    froot = 'adult_R'
    max_accuracy = 0.835
    max_prefix_length = 3
    garbage_collect = True
    seed = 0
    sample = 0.1    # 10% of the dataset

    cache size: [1, 257, 32129, 2571505]
    dead prefix start: [0, 0, 0, 0]
    caputed zero: [0, 0, 326, 72215]
    stunted prefix: [0, 0, 0, 0]
    commutes: [0, 0, 7232, 963103]
    dead prefix: [0, 27, 8041, 1313416]
    inferior: [0, 0, 25003, 4140139]
    seconds: [0.0, 0.01, 1.31, 148.49]
    growth: [257, 125, 80]

    if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
    else if {marital.status=Married,occupation=Prof-specialty} then predict 0
    else if {marital.status=Married,occupation=Exec-managerial} then predict 0
    else predict 1

    prefix: (168, 106, 199)
    prediction: (0, 0, 0)
    accuracy: 0.829
    upper_bound: 0.955
    num_captured: 519
    num_captured_correct: 385
    sum(not_captured): 2489
    curiosity: 0.258


### adult w/full dataset is similar

    froot = 'adult_R'
    warm_start = True
    froot = 'adult_R'
    max_accuracy = 0.834
    max_prefix_length = 3
    garbage_collect = True
    # full dataset

    cache size: [1, 258, 32232, 2594146]
    dead prefix start: [0, 0, 0, 0]
    caputed zero: [0, 0, 577, 140941]
    stunted prefix: [0, 0, 0, 0]
    dead prefix: [0, 26, 8736, 1348177]
    inferior: [0, 0, 31469, 5006160]
    seconds: [0.0, 4.91, 4.16, 640.08]

    prefix: (168, 106, 199)
    prediction: (0, 0, 0)
    accuracy: 0.826
    upper_bound: 0.953
    num_captured: 5028
    num_captured_correct: 3622
    sum(not_captured): 25053
    curiosity: 0.280

## serial_priority.py

##### Breadth-first branch-and-bound algorithm with cache

    def incremental(prefix, rules, labels, min_objective, *cache):
        ...
        return objective

    def branch_and_bound(rules, labels):
        initialize queue (with () for cold start)
        initialize cache (empty for cold start)
        initialize min_objective (inf for cold start)
        done = False

        while(queue and not done):
            prefix_start = pop(queue)
            rule_list = [r for r in range(len(rules)) if r not in prefix_start]

            for r in rule_list:
                prefix = prefix_start + (r,)
                (objective, lower_bound) = incremental(prefix, rules, labels, min_objective, *cache)

                if (lower_bound < min_objective):
                    push(queue, prefix)

                if (objective < min_objective):
                    (min_objective, best_prefix) = (objective, prefix)

                    if (objective is optimal for its length):
                        done = True

        return (min_objective, best_prefix)

#### Branch-and-bound algorithm with priority queue, cache, and garbage collection

    def incremental(prefix, rules, labels, min_objective, *cache):

        min_correct = minimum number of data each rule in a rule list must capture and predict correctly

        num_captured = calculate_captures(prefix, rules, *cache)
        if (num_captured == 0):
            return None    # the last rule doesn't capture any new data points
        if (num_captured < min_correct):
            return None    # last rule doesn't capture enough new data

        (num_captured_correct, not_captured) = calculate_correct(prefix, labels, *cache)
        if (num_captured_correct < min_correct):
            return None    # last rule doesn't correctly predict enough new data

        calculate default_rule, objective, lower_bound

        if (lower_bound > min_objective):
            return None    # dead prefix

        if (cache contains permutation of prefix with better objective):
            return None    # symmetry-aware garbage collection

        cache the prefix and associated computation
        return objective

    def branch_and_bound(rules, labels, policy):
        initialize priority_queue (with () for cold start)
        initialize cache (empty for cold start)
        initialize min_objective (inf for cold start)
        done = False

        while(priority_queue and not done):
            prefix_start = pop(priority_queue)
            if prefix_start not in cache:    # we garbage collect cache but not priority_queue
                continue
            cached_prefix = cache[prefix_start]
            if (cached_prefix.lower_bound > min_objective):    # dead prefix start
                continue

            rule_list = [r for r in range(len(rules)) if r not in prefix_start]
            pruned_rule_list = prune_rules(prefix, rule_list, rules)    # symmetry-aware pruning

            for r in pruned_rule_list:
                prefix = prefix_start + (r,)
                objective = incremental(prefix, rules, labels, min_objective, *cache)
                if (objective is None):    # prefix is useless
                    continue

                if (objective < min_objective):
                    (min_objective, best_prefix) = (objective, prefix)
                    garbage_collect(min_objective, *cache)    # eject entries with lower_bound > min_objective

                if (prefix is optimal for its length):
                    if (policy is breadth-first):    # found an optimal prefix
                        done = True
                    else:                            # switch to certification mode
                        policy = breadth first
                        priority_queue = reprioritize(priority_queue, policy)
                else:
                    push(priority_queue, policy, prefix)

            if (policy is not breadth-first):
                if (prefix_start is a dead end):    # prefix_start has no useful children
                    prune_up(prefix_start, *cache)  # remove prefix_start and dead end ancestors

        return (min_objective, best_prefix)


    adult, method=curiosity, sample=0.1
    c=0.01
    min_cap=0.003
    min_objective=0.08
    -> inconclusive, > 3,000,000 prefixes w/ lower bound < 0.08
    adult_R-serial_priority-c=0.01000-min_cap=0.003-min_objective=0.080-method=curiosity-max_cache_size=3000000-sample=0.10-cache

    adult, method=curiosity, sample=0.1
    c=0.01
    min_cap=0.003
    min_objective=0.05
    -> certified zero prefixes w/ objective < 0.05
    -> 156,603 prefixes w/ lower bound < 0.05, max prefix length = 4
    adult_R-serial_priority-c=0.01000-min_cap=0.003-min_objective=0.050-method=curiosity-max_cache_size=3000000-sample=0.10-max_length=4

    adult, method=curiosity, sample=0.1
    c=0.01
    min_cap=0.003
    min_objective=0.1
    -> inconclusive, > 3,000,000 prefixes w/ lower bound < 0.1
        adult_R-serial_priority-c=0.01000-min_cap=0.003-min_objective=0.100-method=curiosity-max_cache_size=3000000-sample=0.10-cache

    adult, method=curiosity, sample=0.1
    c=0.003
    min_cap=0.003
    min_objective=0.05
    -> inconclusive, > 3,000,000 prefixes w/ lower bound < 0.05
    adult_R-serial_priority-c=0.00300-min_cap=0.003-min_objective=0.050-method=curiosity-max_cache_size=3000000-sample=0.10-max_length=7

    adult, method=curiosity, sample=0.1
    c=0.0
    min_cap=0.003
    min_objective=0.01
    -> inconclusive, > 3,000,000 prefixes w/ lower bound < 0.01
    adult_R-serial_priority-c=0.00000-min_cap=0.003-min_objective=0.010-method=curiosity-max_cache_size=3000000-sample=0.10-max_length=13

    adult, method=curiosity, sample=0.1
    c=0.0
    min_cap=0.003
    min_objective=0.005
    -> certified zero prefixes w/ objective < 0.005
    -> 166,313 prefixes w/ lower bound < 0.005, max prefix length = 11
        adult_R-serial_priority-c=0.00000-min_cap=0.003-min_objective=0.005-method=curiosity-max_cache_size=3000000-sample=0.10-cache

### adult w/objective-based prioritization

    method = 'objective'
    max_cache_size = 3000000
    froot = 'adult_R'
    max_accuracy = None
    min_objective = None
    c = 0.
    max_prefix_length = 70  # not an actual constraint
    seed = 0
    sample = 0.1

    if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
    else if {education=Bachelors,marital.status=Married} then predict 0
    else if {marital.status=Married,occupation=Prof-specialty} then predict 0
    else if {marital.status=Married,occupation=Exec-managerial} then predict 0
    else if {age=Middle-aged,capital.gain=capital-gainEQ0} then predict 1
    else if {relationship=Husband,hours.per.week=Over-time} then predict 0
    else if {education=Grad-school,marital.status=Married} then predict 0
    else if {age=Middle-aged,capital.loss=capital-lossEQ0} then predict 1
    else if {education=Grad-school,sex=Male} then predict 0
    else if {age=Senior,capital.gain=capital-gainEQ0} then predict 1
    else if {age=Senior,occupation=Exec-managerial} then predict 1
    else if {capital.gain=capital-gainEQ0,hours.per.week=Part-time} then predict 1
    else if {age=Young,relationship=Own-child} then predict 1
    else if {marital.status=Never-married,relationship=Own-child} then predict 0
    else if {capital.loss=capital-lossEQ0,hours.per.week=Part-time} then predict 1
    else if {education=Assoc-degree,capital.gain=capital-gainEQ0} then predict 1
    else if {education=Assoc-degree,capital.loss=capital-lossEQ0} then predict 1
    else if {marital.status=Never-married,hours.per.week=Full-time} then predict 1
    else if {education=Grad-school,capital.gain=capital-gainEQ0} then predict 1
    else if {marital.status=Never-married,sex=Male} then predict 1
    else if {occupation=Exec-managerial,capital.gain=capital-gainEQ0} then predict 0
    else if {education=Bachelors,sex=Male} then predict 0
    else if {sex=Male,hours.per.week=Over-time} then predict 0
    else if {education=Bachelors,hours.per.week=Full-time} then predict 1
    else if {marital.status=Not-married-anymore,capital.gain=capital-gainEQ0} then predict 1
    else if {relationship=Not-in-family,sex=Male} then predict 0
    else if {education=HS-grad,marital.status=Never-married} then predict 1
    else if {education=HS-grad,sex=Female} then predict 1
    else if {race=Black,capital.gain=capital-gainEQ0} then predict 0
    else if {age=Young,hours.per.week=Full-time} then predict 1
    else if {workclass=Gov,capital.gain=capital-gainEQ0} then predict 0
    else if {age=Young,marital.status=Never-married} then predict 1
    else if {capital.gain=capital-gainEQ0,hours.per.week=Full-time} then predict 1
    else if {marital.status=Not-married-anymore,hours.per.week=Full-time} then predict 1
    else if {age=Senior,workclass=Private} then predict 0
    else if {education=Grad-school,capital.loss=capital-lossEQ0} then predict 0
    else if {occupation=Craft-repair,capital.gain=capital-gainEQ0} then predict 0
    else if {age=Senior,capital.loss=capital-lossEQ0} then predict 1
    else if {workclass=Private,capital.loss=capital-lossEQ0} then predict 1
    else predict 0
    prefix: (43, 69, 122, 121, 0, 206, 77, 1, 81, 20, 26, 49, 38, 134, 54, 57, 58, 130, 75, 136, 160, 73, 240, 67, 138, 217, 87, 91, 189, 34, 243, 35, 47, 140, 30, 76, 153, 21, 253)
    prediction: (0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1)
    accuracy: 0.8447473404
    upper_bound: 0.8447473404
    objective: 467.0000000000
    lower_bound: 467.0000000000
    num_captured: 3006
    num_captured_correct: 2539
    sum(not_captured): 2
    curiosity: 0.155

    Prefix evaluated on the full dataset:
    prediction: (0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1)
    accuracy: 0.8327515708
    upper_bound: 0.8328513015
    objective: 5031.0000000000
    lower_bound: 5028.0000000000
    num_captured: 30064
    num_captured_correct: 25036
    sum(not_captured): 17
    curiosity: 0.167

    method = 'objective'
    max_cache_size = 3000000
    froot = 'adult_R'
    max_accuracy = None
    min_objective = None
    c = 0.
    max_prefix_length = 70  # not an actual constraint
    seed = 0
    sample = 0.1

    if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
    else if {education=Bachelors,marital.status=Married} then predict 0
    else if {marital.status=Married,occupation=Prof-specialty} then predict 0
    else if {marital.status=Married,occupation=Exec-managerial} then predict 0
    else if {education=Grad-school,marital.status=Married} then predict 0
    else if {age=Middle-aged,capital.gain=capital-gainEQ0} then predict 1
    else if {education=Assoc-degree,relationship=Husband} then predict 0
    else if {age=Middle-aged,capital.loss=capital-lossEQ0} then predict 1
    else if {capital.gain=capital-gainEQ0,capital.loss=capital-lossEQ0} then predict 1
    else if {education=Some-college,marital.status=Married} then predict 0
    else if {age=Senior,capital.gain=capital-gainEQ0} then predict 1
    else if {education=Grad-school,capital.gain=capital-gainEQ0} then predict 0
    else if {age=Senior,capital.loss=capital-lossEQ0} then predict 1
    else if {capital.gain=capital-gainEQ0,hours.per.week=Full-time} then predict 1
    else if {age=Young,capital.gain=capital-gainEQ0} then predict 1
    else if {age=Young,capital.loss=capital-lossEQ0} then predict 1
    else if {occupation=Exec-managerial,hours.per.week=Over-time} then predict 0
    else if {capital.gain=capital-gainEQ0,hours.per.week=Over-time} then predict 1
    else if {capital.gain=capital-gainEQ0,native.country=N-America} then predict 1
    else if {workclass=Private,occupation=Exec-managerial} then predict 0
    else if {capital.gain=capital-gainEQ0,hours.per.week=Part-time} then predict 1
    else if {capital.loss=capital-lossEQ0,hours.per.week=Part-time} then predict 1
    else if {education=Assoc-degree,capital.loss=capital-lossEQ0} then predict 1
    else if {marital.status=Married,occupation=Craft-repair} then predict 1
    else if {education=Bachelors,capital.loss=capital-lossEQ0} then predict 1
    else if {marital.status=Married,occupation=Sales} then predict 1
    else if {occupation=Sales,race=White} then predict 0
    else if {education=Grad-school,capital.loss=capital-lossEQ0} then predict 1
    else if {marital.status=Never-married,capital.loss=capital-lossEQ0} then predict 1
    else if {education=HS-grad,capital.loss=capital-lossEQ0} then predict 1
    else if {workclass=Private,marital.status=Married} then predict 0
    else if {capital.loss=capital-lossEQ0,hours.per.week=Over-time} then predict 1
    else if {education=Some-college,capital.loss=capital-lossEQ0} then predict 1
    else if {marital.status=Not-married-anymore,capital.loss=capital-lossEQ0} then predict 1
    else if {workclass=Gov,capital.loss=capital-lossEQ0} then predict 1
    else if {capital.loss=capital-lossEQ0,hours.per.week=Full-time} then predict 0
    else predict 1
    prefix: (43, 69, 122, 121, 77, 0, 62, 1, 46, 97, 20, 75, 21, 47, 32, 33, 162, 48, 50, 266, 49, 54, 58, 120, 66, 123, 185, 76, 129, 84, 260, 53, 95, 139, 244, 52)
    prediction: (0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0)
    accuracy: 0.8343140188
    upper_bound: 0.8343140188
    objective: 4984.0000000000
    lower_bound: 4984.0000000000
    num_captured: 30080
    num_captured_correct: 25096
    sum(not_captured): 1
    curiosity: 0.166

## from Hongyu

A rule list from the latest `sbrl` R pkg :

    sbrl_model <- sbrl(data, iters=20000, pos_sign="1", neg_sign="0", rule_minlen=1, rule_maxlen=2, minsupport_pos=0.10, minsupport_neg=0.10, lambda=20.0, eta=1.0, nchain=25)
    print(sbrl_model)

The rules list is :

    If      {capital.gain=7298LessThancapital-gain} (rule[46]) then positive probability = 0.01617922
    else if {education=Grad-school,marital.status=Married} (rule[76]) then positive probability = 0.24616368
    else if {age=Young,marital.status=Never-married} (rule[36]) then positive probability = 0.99606078
    else if {age=Young,capital.loss=capital-lossEQ0} (rule[34]) then positive probability = 0.92338388
    else if {education=Bachelors,marital.status=Married} (rule[68]) then positive probability = 0.33762434
    else if {marital.status=Married,occupation=Exec-managerial} (rule[123]) then positive probability = 0.46758105
    else if {education=HS-grad,marital.status=Married} (rule[85]) then positive probability = 0.70224325
    else if {education=Some-college,marital.status=Married} (rule[98]) then positive probability = 0.58744545
    else if {relationship=Own-child,hours.per.week=Full-time} (rule[224]) then positive probability = 0.98528471
    else if {marital.status=Married,occupation=Prof-specialty} (rule[124]) then positive probability = 0.27289720
    else if {education=Assoc-degree,marital.status=Married} (rule[59]) then positive probability = 0.57581069
    else if {capital.loss=capital-lossEQ0,hours.per.week=Part-time} (rule[55]) then positive probability = 0.98307380
    else if {occupation=Other-service,capital.loss=capital-lossEQ0} (rule[172]) then positive probability = 0.97980381
    else if {occupation=Prof-specialty,sex=Male} (rule[183]) then positive probability = 0.73821990
    else if {occupation=Adm-clerical,sex=Female} (rule[154]) then positive probability = 0.98090186
    else if {occupation=Prof-specialty} (rule[184]) then positive probability = 0.86271186
    else if {age=Middle-aged,education=HS-grad} (rule[4]) then positive probability = 0.96911197
    else if {education=Grad-school} (rule[81]) then positive probability = 0.61656442
    else if {age=Middle-aged,hours.per.week=Full-time} (rule[6]) then positive probability = 0.94713161
    else if {education=Bachelors,native.country=N-America} (rule[69]) then positive probability = 0.73352034
    else if {sex=Male,native.country=N-America} (rule[244]) then positive probability = 0.86269540
    else  (default rule)  then positive probability = 0.94477711

Elaine seems to have a slightly different rule list, without a rule for `{occupation=Adm-clerical,sex=Female}` :

    line numbers: (46, 78, 36, 34, 70, 122, 87, 98, 222, 123, 60, 55, 170, 181, ???, 182, ...)

    zero-indexed: (45, 77, 35, 33, 69, 121, 86, 97, 221, 122, 59, 54, 169, 180)


There is another example rule list in our earlier paper http://arxiv.org/pdf/1602.08610v1.pdf on page 3:

    if capital-gain>$7298.00 then probability to make over 50K = 0.986
    else if Young,Never-married, then probability to make over 50K = 0.003
    else if Grad-school,Married, then probability to make over 50K = 0.748
    else if Young,capital-loss=0, then probability to make over 50K = 0.072
    else if Own-child,Never-married, then probability to make over 50K = 0.015
    else if Bachelors,Married, then probability to make over 50K = 0.655
    else if Bachelors,Over-time, then probability to make over 50K = 0.255
    else if Exec-managerial,Married, then probability to make over 50K = 0.531
    else if Married,HS-grad, then probability to make over 50K = 0.300
    else if Grad-school, then probability to make over 50K = 0.266
    else if Some-college,Married, then probability to make over 50K = 0.410
    else if Prof-specialty,Married, then probability to make over 50K = 0.713
    else if Assoc-degree,Married, then probability to make over 50K = 0.420
    else if Part-time, then probability to make over 50K = 0.013
    else if Husband, then probability to make over 50K = 0.126
    else if Prof-specialty, then probability to make over 50K = 0.148
    else if Exec-managerial,Male, then probability to make over 50K = 0.193
    else if Full-time,Private, then probability to make over 50K = 0.026
    else (default rule) then probability to make over 50K = 0.066

    line numbers: (46, 36, 78, 34, 135, 70, 69, 122, 87, 83, 98, 123, 60, 114, 211, 182, 167, 258)

    zero-indexed: (45, 35, 77, 33, 134, 69, 68, 121, 86, 82, 97, 122, 59, 113, 210, 181, 166, 257)
