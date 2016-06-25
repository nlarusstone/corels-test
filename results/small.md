##small datasets (with varying amounts of regularization)

| dataset | c | d | time (s) | objective | lower bound | accuracy | upper bound | length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| monks3 | 0.010 | 0.010 | 0.006 | 0.048 | 0.048 | 0.972 | 0.972 | 2 |
| monks3 | 0.003 | 0.000 | 0.006 | 0.018 | 0.018 | 1.000 | 1.000 | 6 |
| monks3 | 0.001 | 0.000 | 0.007 | 0.006 | 0.006 | 1.000 | 1.000 | 6 |
| monks3 | 0.000 | 0.000 | 0.006 | 0.000 | 0.000 | 1.000 | 1.000 | 7 |
| votes | 0.010 | 0.010 | 0.002 | 0.054 | 0.042 | 0.956 | 0.968 | 1 |
| votes | 0.003 | 0.000 | 0.019 | 0.047 | 0.035 | 0.956 | 0.968 | 1 |
| votes | 0.001 | 0.000 | 0.300 | 0.042 | 0.042 | 0.966 | 0.966 | 8 |
| votes | 0.000 | 0.000 | 0.015 | 0.034 | 0.034 | 0.966 | 0.966 | 10 |

###monks3, c=0.010, d=0.010

	if {a5=4} then predict 0
	else if {a2=3} then predict 0
	else predict 1

###monks3, c=0.003, d=0.000

	if {a5=4} then predict 0
	else if {a2=2} then predict 1
	else if {a2=1} then predict 1
	else if {a4=3} then predict 0
	else if {a4=2} then predict 0
	else if {a5=3} then predict 1
	else predict 0

###monks3, c=0.001, d=0.000

	if {a5=4} then predict 0
	else if {a2=2} then predict 1
	else if {a2=1} then predict 1
	else if {a4=3} then predict 0
	else if {a4=2} then predict 0
	else if {a5=3} then predict 1
	else predict 0

###monks3, c=0.000, d=0.000

	if {a5=4} then predict 0
	else if {a2=2} then predict 1
	else if {a2=1} then predict 1
	else if {a4=2} then predict 0
	else if {a5=1} then predict 0
	else if {a4=3} then predict 0
	else if {a5=2} then predict 0
	else predict 1

###votes, c=0.010, d=0.010

	if {V4} then predict 0
	else predict 1

###votes, c=0.003, d=0.000

	if {V4} then predict 0
	else predict 1

###votes, c=0.001, d=0.000

	if {V4} then predict 0
	else if {V3} then predict 1
	else if {V15} then predict 1
	else if {V5} then predict 1
	else if {V11} then predict 1
	else if {V1} then predict 0
	else if {V12} then predict 0
	else if {V9} then predict 1
	else predict 0

###votes, c=0.000, d=0.000

	if {V4} then predict 0
	else if {V3} then predict 1
	else if {V11} then predict 1
	else if {V2} then predict 1
	else if {V15} then predict 1
	else if {V5} then predict 1
	else if {V1} then predict 0
	else if {V7} then predict 1
	else if {V6} then predict 0
	else if {V9} then predict 1
	else predict 0
