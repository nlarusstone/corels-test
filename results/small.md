##small datasets (with varying amounts of regularization)

| dataset | c | d | time (s) | objective | lower bound | accuracy | upper bound | length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bcancer | 0.010 | 0.010 | 1.312 | 0.068 | 0.067 | 0.952 | 0.953 | 2 |
| bcancer | 0.003 | 0.000 | 43.007 | 0.047 | 0.046 | 0.965 | 0.966 | 4 |
| bcancer | 0.001 | 0.000 | 172.292 | 0.034 | 0.034 | 0.977 | 0.977 | 11 |
| bcancer | 0.000 | 0.000 | 1250.313 | 0.022 | 0.022 | 0.978 | 0.978 | 16 |
| cars | 0.010 | 0.010 | 0.272 | 0.131 | 0.113 | 0.939 | 0.957 | 7 |
| cars | 0.003 | 0.000 | 0.140 | 0.079 | 0.076 | 0.948 | 0.951 | 9 |
| cars | 0.001 | 0.000 | 0.153 | 0.061 | 0.060 | 0.950 | 0.951 | 11 |
| cars | 0.000 | 0.000 | 0.187 | 0.049 | 0.049 | 0.951 | 0.951 | 13 |
| haberman | 0.010 | 0.010 | 4.839 | 0.259 | 0.056 | 0.761 | 0.964 | 2 |
| haberman | 0.003 | 0.000 | 30.551 | 0.230 | 0.230 | 0.794 | 0.794 | 8 |
| haberman | 0.001 | 0.000 | 40.338 | 0.214 | 0.214 | 0.794 | 0.794 | 8 |
| haberman | 0.000 | 0.000 | 46.211 | 0.206 | 0.157 | 0.794 | 0.843 | 9 |
| monks1 | 0.010 | 0.010 | 0.049 | 0.207 | 0.207 | 0.833 | 0.833 | 4 |
| monks1 | 0.003 | 0.000 | 0.049 | 0.179 | 0.179 | 0.833 | 0.833 | 4 |
| monks1 | 0.001 | 0.000 | 0.047 | 0.171 | 0.171 | 0.833 | 0.833 | 4 |
| monks1 | 0.000 | 0.000 | 0.052 | 0.167 | 0.167 | 0.833 | 0.833 | 5 |
| monks2 | 0.010 | 0.010 | 2.414 | 0.333 | 0.333 | 0.727 | 0.727 | 6 |
| monks2 | 0.003 | 0.000 | 1.887 | 0.291 | 0.291 | 0.727 | 0.727 | 6 |
| monks2 | 0.001 | 0.000 | 2.275 | 0.279 | 0.279 | 0.727 | 0.727 | 6 |
| monks2 | 0.000 | 0.000 | 1.832 | 0.273 | 0.273 | 0.727 | 0.727 | 6 |
| monks3 | 0.010 | 0.010 | 0.005 | 0.048 | 0.048 | 0.972 | 0.972 | 2 |
| monks3 | 0.003 | 0.000 | 0.006 | 0.018 | 0.018 | 1.000 | 1.000 | 6 |
| monks3 | 0.001 | 0.000 | 0.006 | 0.006 | 0.006 | 1.000 | 1.000 | 6 |
| monks3 | 0.000 | 0.000 | 0.004 | 0.000 | 0.000 | 1.000 | 1.000 | 7 |
| votes | 0.010 | 0.010 | 0.003 | 0.054 | 0.042 | 0.956 | 0.968 | 1 |
| votes | 0.003 | 0.000 | 0.033 | 0.047 | 0.035 | 0.956 | 0.968 | 1 |
| votes | 0.001 | 0.000 | 0.311 | 0.042 | 0.042 | 0.966 | 0.966 | 8 |
| votes | 0.000 | 0.000 | 0.015 | 0.034 | 0.034 | 0.966 | 0.966 | 10 |

###bcancer, c=0.010, d=0.010

	if {a6>7} then predict 1
	else if {a2<5} then predict 0
	else predict 1

![bcancer_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/bcancer_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###bcancer, c=0.003, d=0.000

	if {a1>7} then predict 1
	else if {a8>7} then predict 1
	else if {a6>7} then predict 1
	else if {a2<5} then predict 0
	else predict 1

![bcancer_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/bcancer_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![bcancer_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/bcancer_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###bcancer, c=0.001, d=0.000

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

![bcancer_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/bcancer_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![bcancer_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/bcancer_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###bcancer, c=0.000, d=0.000

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

![bcancer_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/bcancer_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![bcancer_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/bcancer_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

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

###haberman, c=0.010, d=0.010

	if {age<40} then predict 1
	else if {nodes10-19} then predict 0
	else predict 1

![haberman_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/haberman_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![haberman_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/haberman_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###haberman, c=0.003, d=0.000

	if {age<40} then predict 1
	else if {nodes0} then predict 1
	else if {year>65} then predict 1
	else if {nodes10-19} then predict 0
	else if {age>69} then predict 0
	else if {nodes1-9} then predict 1
	else if {year62-63} then predict 0
	else if {age60-69} then predict 1
	else predict 0

![haberman_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/haberman_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![haberman_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/haberman_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###haberman, c=0.001, d=0.000

	if {age<40} then predict 1
	else if {nodes0} then predict 1
	else if {year>65} then predict 1
	else if {nodes10-19} then predict 0
	else if {age>69} then predict 0
	else if {nodes1-9} then predict 1
	else if {year62-63} then predict 0
	else if {age60-69} then predict 1
	else predict 0

![haberman_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/haberman_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![haberman_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/haberman_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###haberman, c=0.000, d=0.000

	if {age<40} then predict 1
	else if {year>65} then predict 1
	else if {nodes>29} then predict 0
	else if {nodes10-19} then predict 0
	else if {nodes0} then predict 1
	else if {age60-69} then predict 1
	else if {nodes20-29} then predict 0
	else if {year62-63} then predict 1
	else if {age>69} then predict 0
	else predict 1

![haberman_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/haberman_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![haberman_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/haberman_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks1, c=0.010, d=0.010

	if {a5=1} then predict 1
	else if {a1=2} then predict 0
	else if {a1=1} then predict 0
	else if {a2=3} then predict 1
	else predict 0

![monks1_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks1_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks1_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks1_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks1, c=0.003, d=0.000

	if {a5=1} then predict 1
	else if {a1=2} then predict 0
	else if {a1=1} then predict 0
	else if {a2=3} then predict 1
	else predict 0

![monks1_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks1_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks1_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks1_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks1, c=0.001, d=0.000

	if {a5=1} then predict 1
	else if {a1=2} then predict 0
	else if {a1=1} then predict 0
	else if {a2=3} then predict 1
	else predict 0

![monks1_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks1_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks1_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks1_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks1, c=0.000, d=0.000

	if {a5=1} then predict 1
	else if {a1=1} then predict 0
	else if {a2=1} then predict 0
	else if {a1=2} then predict 1
	else if {a2=2} then predict 0
	else predict 1

![monks1_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks1_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks1_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks1_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks2, c=0.010, d=0.010

	if {a1=1} then predict 0
	else if {a3=2} then predict 0
	else if {a2=1} then predict 0
	else if {a4=1} then predict 0
	else if {a6=1} then predict 1
	else if {a5=1} then predict 1
	else predict 0

![monks2_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks2_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###monks2, c=0.003, d=0.000

	if {a1=1} then predict 0
	else if {a3=2} then predict 0
	else if {a2=1} then predict 0
	else if {a4=1} then predict 0
	else if {a6=1} then predict 1
	else if {a5=1} then predict 1
	else predict 0

![monks2_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks2_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###monks2, c=0.001, d=0.000

	if {a5=1} then predict 0
	else if {a1=1} then predict 0
	else if {a3=2} then predict 0
	else if {a2=1} then predict 0
	else if {a6=1} then predict 1
	else if {a4=1} then predict 1
	else predict 0

![monks2_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks2_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###monks2, c=0.000, d=0.000

	if {a5=1} then predict 0
	else if {a1=1} then predict 0
	else if {a3=2} then predict 0
	else if {a2=1} then predict 0
	else if {a6=1} then predict 1
	else if {a4=1} then predict 1
	else predict 0

![monks2_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks2_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###monks3, c=0.010, d=0.010

	if {a5=4} then predict 0
	else if {a2=3} then predict 0
	else predict 1

![monks3_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks3_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###monks3, c=0.003, d=0.000

	if {a5=4} then predict 0
	else if {a2=2} then predict 1
	else if {a2=1} then predict 1
	else if {a4=3} then predict 0
	else if {a4=2} then predict 0
	else if {a5=3} then predict 1
	else predict 0

![monks3_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks3_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks3_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks3_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks3, c=0.001, d=0.000

	if {a5=4} then predict 0
	else if {a2=2} then predict 1
	else if {a2=1} then predict 1
	else if {a4=3} then predict 0
	else if {a4=2} then predict 0
	else if {a5=3} then predict 1
	else predict 0

![monks3_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks3_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks3_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks3_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###monks3, c=0.000, d=0.000

	if {a5=4} then predict 0
	else if {a2=2} then predict 1
	else if {a2=1} then predict 1
	else if {a4=2} then predict 0
	else if {a5=1} then predict 0
	else if {a4=3} then predict 0
	else if {a5=2} then predict 0
	else predict 1

![monks3_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/monks3_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![monks3_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/monks3_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

###votes, c=0.010, d=0.010

	if {V4} then predict 0
	else predict 1

![votes_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/votes_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

###votes, c=0.003, d=0.000

	if {V4} then predict 0
	else predict 1

![votes_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/votes_R-serial_priority-c=0.00300-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)

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

![votes_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/votes_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![votes_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/votes_R-serial_priority-c=0.00100-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)

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

![votes_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log](../figs/votes_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-log.png)
![votes_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache](../figs/votes_R-serial_priority-c=0.00000-min_cap=0.000-min_objective=1.000-method=curiosity-max_cache_size=3000000-sample=1.00-cache.png)
