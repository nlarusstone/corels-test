##small datasets (with varying amounts of regularization)

| dataset | c | d | time (s) | objective | lower bound | accuracy | upper bound | length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cars | 0.010 | 0.010 | 0.199 | 0.131 | 0.113 | 0.939 | 0.957 | 7 |
| cars | 0.003 | 0.000 | 0.154 | 0.079 | 0.076 | 0.948 | 0.951 | 9 |
| cars | 0.001 | 0.000 | 0.106 | 0.061 | 0.060 | 0.950 | 0.951 | 11 |
| cars | 0.000 | 0.000 | 0.101 | 0.049 | 0.049 | 0.951 | 0.951 | 13 |

###cars, c=0.010, d=0.010

	if {persons=2} then predict 0
	else if {safety=low} then predict 0
	else if {buying=low} then predict 1
	else if {buying=med} then predict 1
	else if {maint=vhigh} then predict 0
	else if {safety=high} then predict 1
	else if {lug-boot=small} then predict 0
	else predict 1

![cars_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/cars_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![cars_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/cars_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###cars, c=0.003, d=0.000

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

![cars_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/cars_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![cars_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/cars_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###cars, c=0.001, d=0.000

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

![cars_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/cars_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![cars_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/cars_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###cars, c=0.000, d=0.000

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

![cars_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/cars_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![cars_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/cars_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)
