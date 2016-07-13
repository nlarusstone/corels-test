##small datasets (c=0.010, max_cache_size=2000000)

expanded with maximum cardinality = 2 and minimum support = 10%

| dataset | method | time (s) | cache | queue | objective | lower bound | accuracy | upper bound | length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bcancer | breadth_first | 143.044 | 2000126 | 2000897 | 0.055 | 0.049 | 0.965 | 0.971 | 2 |
| bcancer | curiosity | 433.993 | 2000180 | 2038087 | 0.058 | 0.050 | 0.952 | 0.960 | 1 |
| cars | breadth_first | 199.885 | 2000003 | 2171492 | 0.113 | 0.113 | 0.917 | 0.917 | 3 |
| cars | curiosity | 82.147 | 2000364 | 2041731 | 0.115 | 0.061 | 0.925 | 0.979 | 4 |
| haberman | breadth_first | 120.508 | 2000109 | 2098623 | 0.245 | 0.239 | 0.775 | 0.781 | 2 |
| haberman | curiosity | 70.549 | 2000211 | 1995591 | 0.249 | 0.033 | 0.761 | 0.977 | 1 |
| monks1 | breadth_first | 193.371 | 677148 | 961913 | 0.040 | 0.040 | 1.000 | 1.000 | 4 |
| monks1 | curiosity | 3.033 | 948 | 0 | 0.040 | 0.040 | 1.000 | 1.000 | 4 |
| monks2 | breadth_first | 89.244 | 2000031 | 2006327 | 0.331 | 0.261 | 0.699 | 0.769 | 3 |
| monks2 | curiosity | 68.343 | 2000311 | 2005524 | 0.299 | 0.188 | 0.801 | 0.912 | 10 |
| monks3 | breadth_first | 0.080 | 429 | 514 | 0.020 | 0.020 | 1.000 | 1.000 | 2 |
| monks3 | curiosity | 0.035 | 49 | 0 | 0.020 | 0.020 | 1.000 | 1.000 | 2 |
| votes | breadth_first | 423.369 | 121586 | 0 | 0.054 | 0.021 | 0.956 | 0.989 | 1 |
| votes | curiosity | 687.338 | 10 | 0 | 0.054 | 0.021 | 0.956 | 0.989 | 1 |

###bcancer, breadth_first

	if {a8<5:0,a1<5:0} then predict 1
	else if {a6>7:0,a2<5:1} then predict 0
	else predict 1

![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-leaves.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###bcancer, curiosity

	if {a6>7:0,a2<5:1} then predict 0
	else predict 1

![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-leaves.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)

###cars, breadth_first

	if {buying=vhigh:1,maint=low:0} then predict 0
	else if {safety=med:1,lug-boot=small:1} then predict 0
	else if {safety=low:0,persons=2:0} then predict 1
	else predict 0

![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-leaves.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###cars, curiosity

	if {safety=med:0,safety=high:0} then predict 0
	else if {persons=2:1,persons=more:0} then predict 0
	else if {buying=high:1,maint=vhigh:1} then predict 0
	else if {buying=vhigh:1,maint=low:0} then predict 0
	else predict 1

![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-leaves.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)

###haberman, breadth_first

	if {nodes10-19:0,nodes>29:0} then predict 1
	else if {year>65:0,age<40:0} then predict 0
	else predict 1

![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-leaves.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###haberman, curiosity

	if {nodes10-19:1,age<40:0} then predict 0
	else predict 1

![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-leaves.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)

###monks1, breadth_first

	if {a1=2:1,a2=2:1} then predict 1
	else if {a5=1:1,a5=2:0} then predict 1
	else if {a2=1:0,a1=3:0} then predict 0
	else if {a1=1:0,a2=3:0} then predict 0
	else predict 1

![monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-leaves.png)
![monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###monks1, curiosity

	if {a5=1:1,a5=2:0} then predict 1
	else if {a1=3:1,a2=3:0} then predict 0
	else if {a1=2:1,a2=2:0} then predict 0
	else if {a1=1:1,a2=1:0} then predict 0
	else predict 1

![monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/monks1-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)

###monks2, breadth_first

	if {a2=1:1,a3=2:0} then predict 0
	else if {a6=1:0,a1=1:0} then predict 0
	else if {a4=1:0,a5=1:0} then predict 1
	else predict 0

![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###monks2, curiosity

	if {a4=1:1,a1=1:1} then predict 0
	else if {a2=1:1,a1=1:1} then predict 0
	else if {a6=1:0,a3=2:1} then predict 0
	else if {a2=1:1,a4=1:1} then predict 0
	else if {a5=1:1,a3=2:0} then predict 0
	else if {a4=1:1,a6=2:1} then predict 1
	else if {a1=1:1,a6=1:0} then predict 1
	else if {a6=2:1,a2=1:0} then predict 0
	else if {a4=1:1,a3=1:1} then predict 0
	else if {a1=1:1,a3=1:1} then predict 0
	else predict 1

![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-leaves.png)
![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)

###monks3, breadth_first

	if {a5=3:1,a4=1:1} then predict 1
	else if {a2=3:0,a5=4:0} then predict 1
	else predict 0

![monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-leaves.png)
![monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###monks3, curiosity

	if {a2=3:0,a5=4:0} then predict 1
	else if {a5=3:1,a4=1:1} then predict 1
	else predict 0

![monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/monks3-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)

###votes, breadth_first

	if {V4:0} then predict 1
	else predict 0

![votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log](../figs/votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-log.png)
![votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache](../figs/votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2000000-sample=1.00-cache.png)

###votes, curiosity

	if {V4:0} then predict 1
	else predict 0

![votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log](../figs/votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-log.png)
![votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache](../figs/votes-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2000000-sample=1.00-cache.png)
