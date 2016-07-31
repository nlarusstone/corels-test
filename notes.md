# notes
A place to stash older notes, results, etc.

## small datasets without rule expansion (with varying amounts of regularization)

### bcancer (c = 0.01, min_captured_correct = 0.01)

    nrules: 27
    ndata: 683

    seconds: 29.18559

    if {a6>7} then predict 1
    else if {a2<5} then predict 0
    else predict 1

    accuracy: 0.9516837482
    objective: 0.0683162518
    seconds: 1.14501

### bcancer (c = 0.003, min_captured_correct = 0.)

    seconds: 44.94337

    if {a1>7} then predict 1
    else if {a8>7} then predict 1
    else if {a6>7} then predict 1
    else if {a2<5} then predict 0
    else predict 1

    accuracy: 0.9648609078
    objective: 0.0471390922

### bcancer (c = 0.001, min_captured_correct = 0.)

    seconds: 119.64070

    if {a7>7} then predict 1
    else if {a2.5-7} then predict 1
    else if {a4>7} then predict 1
    else if {a6>7} then predict 1
    else if {a1<5} then predict 0
    else if {a9.5-7} then predict 1
    else if {a8>7} then predict 1
    else if {a6.5-7} then predict 1
    else if {a1.5-7} then predict 0
    else if {a7.5-7} then predict 1
    else if {a9<5} then predict 0
    else predict 1

    accuracy: 0.9765739385
    objective: 0.0344260615

### bcancer (c = 0., min_captured_correct = 0.)

    seconds: 1009.41659

    if {a7>7} then predict 1
    else if {a2.5-7} then predict 1
    else if {a4>7} then predict 1
    else if {a6>7} then predict 1
    else if {a1<5} then predict 0
    else if {a9>7} then predict 1
    else if {a9.5-7} then predict 1
    else if {a8>7} then predict 1
    else if {a5>7} then predict 0
    else if {a6.5-7} then predict 1
    else if {a3>7} then predict 0
    else if {a2>7} then predict 1
    else if {a8.5-7} then predict 1
    else if {a5<5} then predict 0
    else if {a7.5-7} then predict 1
    else if {a1.5-7} then predict 1
    else predict 0

    accuracy: 0.9780380673
    objective: 0.0219619327

### cars (c = 0.01, min_captured_correct = 0.01)

    nrules: 21
    ndata: 1728

    seconds: 0.21441

    if {persons=2} then predict 0
    else if {safety=low} then predict 0
    else if {buying=low} then predict 1
    else if {buying=med} then predict 1
    else if {maint=vhigh} then predict 0
    else if {safety=high} then predict 1
    else if {lug-boot=small} then predict 0
    else predict 1

    accuracy: 0.9386574074
    objective: 0.1313425926

###  cars (c = 0.003, min_captured_correct = 0.)

    seconds: 0.17232

    if {persons=2} then predict 0
    else if {safety=low} then predict 0
    else if {buying=low} then predict 1
    else if {buying=med} then predict 1
    else if {maint=vhigh} then predict 0
    else if {buying=high} then predict 1
    else if {maint=high} then predict 0
    else if {safety=high} then predict 1
    else if {lug-boot=small} then predict 0
    else predict 1

    accuracy: 0.9479166667
    objective: 0.0790833333

###  cars (c = 0.001, min_captured_correct = 0.)

    seconds: 0.08900

    if {persons=2} then predict 0
    else if {safety=low} then predict 0
    else if {buying=low} then predict 1
    else if {buying=med} then predict 1
    else if {maint=vhigh} then predict 0
    else if {buying=high} then predict 1
    else if {maint=high} then predict 0
    else if {lug-boot=big} then predict 1
    else if {safety=high} then predict 1
    else if {lug-boot=small} then predict 0
    else if {doors=2} then predict 0
    else predict 1

    accuracy: 0.9502314815
    objective: 0.0607685185

###  cars (c = 0., min_captured_correct = 0.)

    seconds: 0.04759

    if {persons=2} then predict 0
    else if {safety=low} then predict 0
    else if {buying=low} then predict 1
    else if {buying=med} then predict 1
    else if {maint=vhigh} then predict 0
    else if {safety=high} then predict 1
    else if {lug-boot=small} then predict 0
    else if {buying=high} then predict 1
    else if {maint=high} then predict 0
    else if {lug-boot=big} then predict 1
    else if {doors=2} then predict 0
    else if {persons=more} then predict 1
    else if {doors=3} then predict 0
    else predict 1

    accuracy: 0.9513888889
    objective: 0.0486111111

### haberman (c = 0.01, min_captured_correct = 0.01)

    nrules: 15
    ndata: 306

    seconds: 4.09679

    if {age<40} then predict 1
    else if {nodes10-19} then predict 0
    else predict 1

    accuracy: 0.7614379085
    objective: 0.2585620915

### haberman (c = 0.003, min_captured_correct = 0.)

    seconds: 35.42373

    if {age<40} then predict 1
    else if {nodes0} then predict 1
    else if {year>65} then predict 1
    else if {nodes10-19} then predict 0
    else if {age>69} then predict 0
    else if {nodes1-9} then predict 1
    else if {year62-63} then predict 0
    else if {age60-69} then predict 1
    else predict 0

    accuracy: 0.7941176471
    objective: 0.2298823529

### haberman (c = 0.001, min_captured_correct = 0.)

    seconds: 46.61386

    same solution as above

### haberman (c = 0., min_captured_correct = 0.)

    ~same as above

### monks1 (c = 0.01, min_captured_correct = 0.01)

    nrules: 17
    ndata: 432

    seconds: 0.06728

    if {a5=1} then predict 1
    else if {a1=2} then predict 0
    else if {a1=1} then predict 0
    else if {a2=3} then predict 1
    else predict 0

    accuracy: 0.8333333333
    objective: 0.2066666667

### monks1 (c = 0.003, 0.001, 0., min_captured_correct = 0.)

    ~same as above

###  monks2 (c = 0.01, min_captured_correct = 0.01)

    nrules: 17
    ndata: 432

    seconds: 5.79060

    if {a1=1} then predict 0
    else if {a3=2} then predict 0
    else if {a2=1} then predict 0
    else if {a4=1} then predict 0
    else if {a6=1} then predict 1
    else if {a5=1} then predict 1
    else predict 0

    accuracy: 0.7268518519
    upper_bound: 0.7268518519

### monks2 (c = 0.003, 0.001, 0., min_captured_correct = 0.)

    ~same as above

### monks3 (c = 0.01, min_captured_correct = 0.01)

    nrules: 17
    ndata: 432

    seconds: 0.01394

    if {a5=4} then predict 0
    else if {a2=3} then predict 0
    else predict 1

    accuracy: 0.9722222222
    objective: 0.0477777778

### monks3 (c = 0.003, min_captured_correct = 0.)

    seconds: 0.00667

    if {a5=4} then predict 0
    else if {a2=2} then predict 1
    else if {a2=1} then predict 1
    else if {a4=3} then predict 0
    else if {a4=2} then predict 0
    else if {a5=3} then predict 1
    else predict 0

    accuracy: 1.0000000000
    objective: 0.0180000000

### monks3 (c = 0.001, min_captured_correct = 0.)

    seconds: 0.00750

    if {a5=4} then predict 0
    else if {a2=2} then predict 1
    else if {a2=1} then predict 1
    else if {a4=3} then predict 0
    else if {a4=2} then predict 0
    else if {a5=3} then predict 1
    else predict 0

    accuracy: 1.0000000000
    objective: 0.0060000000

### monks3 (c = 0., min_captured_correct = 0.)

    ~same as above

### votes (c = 0.01, min_captured_correct = 0.01)

    nrules: 16
    ndata: 435

    if {V4} then predict 0
    else predict 1

    accuracy: 0.9563218391
    objective: 0.0536781609
    seconds: 0.00188

### votes (c = 0.003, min_captured_correct = 0.)

    ~same as above

### votes (c = 0.001, min_captured_correct = 0.)

    seconds: 0.38524

    if {V4} then predict 0
    else if {V3} then predict 1
    else if {V15} then predict 1
    else if {V5} then predict 1
    else if {V11} then predict 1
    else if {V1} then predict 0
    else if {V12} then predict 0
    else if {V9} then predict 1
    else predict 0

    accuracy: 0.9655172414
    objective: 0.0424827586

### votes (c = 0., min_captured_correct = 0.)

    ~same as above

## tic-tac-toe results

### tdata, breadth-first, no regularization (c = 0.)

* Aggressive "optimistic (lying) warm start" (initialize min_objective = 0.001)
* Finds a minimum length (8 rules) perfect prefix (< 180 sec)

### tdata, curiosity, no regularization (c = 0.)

* Cold start, quickly (< 2 sec) finds a perfect prefix that is very long (68 rules)

### tdata, curiosity, regularization (c = 0.001)

* Cold start, quickly (< 2 sec) finds a perfect prefix of length 10
* Then quickly finds perfect prefixes of length 9, then 8 (< 3 sec)
* Then certifies that the best (perfect) prefix has length 8 (< 225 sec)
* Final cache contains 1776 entries with lower bound < 0.008

## adult results

Subsampling 10% of dataset and `min_captured_correct = max(c, 0.003)` unless
otherwise noted.

### adult, curiosity, no regularization (c = 0.)

* Certifies there are no prefixes with objective < 0.005
* Up to symmetries, ~170,000 prefixes have lower bound < 0.005 (length <= 11)

* Initialize min_objective = 0.01
* Inconclusive, > 3,000,000 prefixes have lower bound < 0.01

### adult, curiosity, regularization (c = 0.003)

* Initialize min_objective = 0.01
* Quickly certifies (< 1 sec) that there are no prefixes with objective < 0.01
* Up to symmetries, 471 prefixes have lower bound < 0.01

* Inconclusive for objective < 0.05
* Up to symmetries, > 3,000,000 prefixes have lower bound < 0.05

### adult, curiosity, regularization (c = 0.01)

* Certifies (< 380 sec) that there are no prefixes with objective < 0.05
* Up to symmetries, ~150,000 prefixes have lower bound < 0.05 (length <= 4)

* Certifies (< 18,000 sec) that there are no prefixes with objective < 0.06
* Up to symmetries, ~1,000,000 prefixes have lower bound < 0.06 (length <= 5)

* Inconclusive for objective < 0.08
* Up to symmetries, > 3,000,000 prefixes have lower bound < 0.08

### adult, curiosity, regularization (c = 0.02)

* Certifies (< 95 sec) there are no prefixes with objective < 0.08
* Certifies (< 240 sec) there are no prefixes with objective < 0.09

### adult, breadth-first, aggressive regularization (min_captured_correct = c)

Reporting cache entries by prefix length (for certified runs, these are entries with lower bound less than the best objective).  Also reporting "growth rate."

* (c = 0.06) Certifies (~180 sec) the best prefix is (69,), max cache size ~130,000, max length checked = 3

    [1, 204, 13513, 114479] -> [204, 66.2, 8.47]

* (c = 0.05) Certifies (~900 sec) the best prefix is (69,), max cache size ~580,000, max length checked = 4

    [1, 220, 18561, 455669, 104964] -> [220, 84.3, 24.5, 0.23]

* (c = 0.04) (>1,000 sec) the best known prefix is (69,), max cache size >5,000,000, max length checked >= 4 (certified there are no prefixes of length 2 or 3 that are better)

    [1, 236, 22893, 957038, >4019841] -> [236, 97.0, 41.8, ...]

* (c = 0.01) the best known prefix (43, 122, 121), objective = 0.20088, max cache size >3,000,000 max length checked >=4 (certified this is the best prefix of length 3)

    [1, 263, 32400, 2478819, >488533 ...] -> [263, 123, 76.5, ...]

### adult, (min_captured_correct = c = 0.01), max cache size = 2,600,000

Reporting number of cache leaves by prefix length (things in priority queue) starting at 1

* breadth-first: 0.20088, completed depth = 3

    [0, 0, 2476944, 88552]

* curiosity: 0.22148, explores too deep too fast, e.g., many prefixes of length 1 unexplored, including (43,)

    [237, 7272, 238092, 1449381, 891552]

* lower bound: 0.20420, explores up to depth 4

    [126, 21855, 512618, 2052639]

* objective: 0.20088, explores up to depth 6

    [262, 228, 1137, 4851, 197921, 2366233]

### adult, curiosity, aggressive regularization (min_captured_correct = c)

* (c = 0.1) Certifies (< 1.5 sec) the best prefix is (51,) -> 1.2 sec
* (c = 0.09) Certifies (< 5 sec) the best prefix is (118,) -> 5.3 sec
* (c = 0.08) Certifies (< 10 sec) the best prefix is (118,) -> 9.6 sec
* (c = 0.07) Certifies (< 25 sec) the best prefix is (118,) -> 23 sec
* (c = 0.06) Certifies (< 210 sec) the best prefix is (69,)
* (c = 0.05) Certifies (< 1,060 sec) the best prefix is (69,)
* (c = 0.04) (< 40,000 sec) the best prefix is (69,)

* (c = 0.03) (cache reaches 3 x 10^6 entries in 170 sec)
* (c = 0.02) (cache reaches 3 x 10^6 entries in 131 sec)

* (c = 0.01) (cache reaches 3 x 10^6 entries in 136 sec)

    (0,)    0.26432 0.74568
    (11,)   0.26199 0.74801
    (23,)   0.25601 0.75399
    (43,)   0.22742 0.78258
    (128, 43, 69)   0.22282 0.80718
    (33, 43, 69)    0.22182 0.80818
    (41, 43, 69)    0.22149 0.80851

* (c = 0.0) (cache reaches 3 x 10^6 entries in 102 sec)
* `lower_bound` priority metric performs similarly

    (0,)    0.25432 0.74568
    (11,)   0.25199 0.74801
    (23,)   0.24601 0.75399
    (43,)   0.21742 0.78258
    (114, 59)   0.21676 0.78324
    (114, 69)   0.20180 0.79820
    (114, 38, 69)   0.20146 0.79854
    (114, 236, 69)  0.19648 0.80352
    (114, 236, 38, 69)  0.19614 0.80386
    (114, 236, 38, 87, 43, 69)  0.19249 0.80751
    (114, 236, 38, 87, 43, 267, 69) 0.19149 0.80851
    (114, 236, 38, 87, 43, 34, 69)  0.19116 0.80884
    (43, 38, 87, 267, 34, 69)   0.19016 0.80984

* (c = 0.01)

  * Certifies (< 12 sec) that there are no prefixes with objective < 0.04
  * Up to symmetries, 0 prefixes have lower bound < 0.04

  * Certifies (< 60 sec) that there are no prefixes with objective < 0.05
  * Up to symmetries, 42 prefixes have lower bound < 0.05 (length <= 2)

  * Certifies (< 650 sec) that there are no prefixes with objective < 0.06
  * Up to symmetries, 569 prefixes have lower bound < 0.06 (length <= 3)

### adult, objective

* (c = 0.) quickly (< 20 sec) finds a good prefix
* (objective = 0.15525, accuracy = 0.84475, length = 39)
* (43, 69, 122, 121, 0, 206, 77, 1, 81, 20, 26, 49, 38, 134, 54, 57, 58, 130, 75, 136, 160, 73, 240, 67, 138, 217, 87, 91, 189, 34, 243, 35, 47, 140, 30, 76, 153, 21, 253)
* No improvement after 500 sec

* Full dataset (c = 0.)
* quickly (~1.0 sec) finds a good prefix (accuracy = 0.83431, length = 36)
* (43, 69, 122, 121, 77, 0, 62, 1, 46, 97, 20, 75, 21, 47, 32, 33, 162, 48, 50, 266, 49, 54, 58, 120, 66, 123, 185, 76, 129, 84, 260, 53, 95, 139, 244, 52)
* No improvement after 500 sec

* Full dataset (c = 0.0001)
* (43, 69, 122, 121, 77, 0, 62, 3, 7, 46, 97)
* (objective = 0.16675, accuracy = 0.83435, seconds < 1)

* Full dataset (c = 0.001)
* (43, 69, 122, 77, 46, 118, 97)
* (objective = 0.17169, accuracy: 0.83531, seconds < 100)

* (c = 0.003) quickly (< 1 sec) finds a good prefix
* (43, 69, 122, 121) (objective = 0.17656, accuracy = 0.83544)
* cache reaches 3 x 10^6 entries in 201 sec

* (c = 0.01) quickly (< 4 sec) finds a good prefix
* (43, 122, 121) (objective = 0.20088, accuracy = 0.82912)
* cache reaches 3 x 10^6 entries in 216 sec

* (c = 0.02) quickly (< 1 sec) finds a good prefix
* (122, 121) (objective = 0.23049, accuracy = 0.80951)
* cache reaches 3 x 10^6 entries in 205 sec

### adult, objective, small subsample (sample = 0.017)

* (c = 0.) (< 14 sec, objective = 0.09198, accuracy = 0.90802, length = 54)
* (122, 121, 43, 69, 59, 0, 4, 2, 12, 77, 8, 16, 49, 73, 32, 33, 54, 57, 130, 81, 75, 76, 162, 26, 91, 87, 128, 174, 175, 67, 254, 65, 144, 150, 6, 18, 1, 96, 102, 147, 97, 94, 168, 219, 244, 243, 156, 143, 85, 120, 196, 276, 105, 182)
* No improvement after 500 sec, cache stays small (< 2000)

### adult, curiosity, warm start

* (c = 0.) (0.15525)
* (c = 0.003) (0.17656)
* (c = 0.01) (0.20088)


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
