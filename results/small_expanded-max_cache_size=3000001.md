##small datasets (c=0.010, max_cache_size=3000001)

expanded with maximum cardinality = 2 and minimum support = 10%

| dataset | method | time (s) | cache | queue | objective | lower bound | accuracy | upper bound | length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bcancer | breadth_first | 228.267 | 3000210 | 2998656 | 0.055 | 0.049 | 0.965 | 0.971 | 2 |
| bcancer | curiosity | 1195.312 | 3000084 | 3062959 | 0.058 | 0.050 | 0.952 | 0.960 | 1 |
| cars | breadth_first | 554.157 | 3000017 | 3939574 | 0.105 | 0.105 | 0.925 | 0.925 | 3 |
| cars | curiosity | 142.292 | 3000245 | 3039643 | 0.115 | 0.061 | 0.925 | 0.979 | 4 |
| haberman | breadth_first | 289.515 | 3000061 | 3360073 | 0.242 | 0.190 | 0.788 | 0.840 | 3 |
| haberman | curiosity | 173.449 | 3000198 | 2994952 | 0.249 | 0.033 | 0.761 | 0.977 | 1 |
| monks2 | breadth_first | 145.278 | 3000166 | 3052809 | 0.317 | 0.271 | 0.713 | 0.759 | 3 |
| monks2 | curiosity | 140.397 | 3000292 | 3003349 | 0.299 | 0.188 | 0.801 | 0.912 | 10 |

###bcancer, breadth_first

	if {a8<5=a8<5:0,a1<5=a1<5:0} then predict 1
	else if {a6>7=a6>7:0,a2<5=a2<5:1} then predict 0
	else predict 1

![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-leaves.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache.png)

###bcancer, curiosity

	if {a6>7=a6>7:0,a2<5=a2<5:1} then predict 0
	else predict 1

![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-leaves.png)
![bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/bcancer-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache.png)

###cars, breadth_first

	if {buying=high=buying=high:1,maint=vhigh=maint=vhigh:1} then predict 0
	else if {buying=vhigh=buying=vhigh:1,maint=low=maint=low:0} then predict 0
	else if {safety=low=safety=low:0,persons=2=persons=2:0} then predict 1
	else predict 0

![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-leaves.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache.png)

###cars, curiosity

	if {safety=med=safety=med:0,safety=high=safety=high:0} then predict 0
	else if {persons=2=persons=2:1,persons=more=persons=more:0} then predict 0
	else if {buying=high=buying=high:1,maint=vhigh=maint=vhigh:1} then predict 0
	else if {buying=vhigh=buying=vhigh:1,maint=low=maint=low:0} then predict 0
	else predict 1

![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-leaves.png)
![cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/cars-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache.png)

###haberman, breadth_first

	if {nodes1-9=nodes1-9:1,age>69=age>69:0} then predict 1
	else if {year>65=year>65:1,age60-69=age60-69:0} then predict 1
	else if {nodes0=nodes0:0,age<40=age<40:0} then predict 0
	else predict 1

![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-leaves.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache.png)

###haberman, curiosity

	if {nodes10-19:1,age<40:0} then predict 0
	else predict 1

![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-leaves.png)
![haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/haberman-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache.png)

###monks2, breadth_first

	if {a6=1:1,a3=2:0} then predict 0
	else if {a4=1:0,a2=1:0} then predict 0
	else if {a1=1:0,a5=1:0} then predict 1
	else predict 0

![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-log.png)
![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=3000001-sample=1.00-cache.png)

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

![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-log.png)
![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-leaves.png)
![monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache](../figs/monks2-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000001-sample=1.00-cache.png)
