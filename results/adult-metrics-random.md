##adult dataset with different priority metrics (c = d = 0.01)

stop after 2,600,000 cache entries

| priority metric | time (s) | objective | lower bound | accuracy | upper bound | best prefix |
| --- | --- | --- | --- | --- | --- | --- |
| breadth_first | 243.988 | 0.201 | 0.075 | 0.829 | 0.955 | (43, 122, 121) |
| curiosity | 132.145 | 0.221 | 0.058 | 0.809 | 0.972 | (41, 43, 69) |
| lower_bound | 120.940 | 0.204 | 0.072 | 0.826 | 0.958 | (43, 179, 121) |
| objective | 212.122 | 0.201 | 0.075 | 0.829 | 0.955 | (43, 122, 121) |

###breadth_first

	if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
	else if {marital.status=Married,occupation=Prof-specialty} then predict 0
	else if {marital.status=Married,occupation=Exec-managerial} then predict 0
	else predict 1

![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2600000-sample=0.10-log](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2600000-sample=0.10-log.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2600000-sample=0.10-cache](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2600000-sample=0.10-cache.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2600000-sample=0.10-leaves](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=breadth_first-max_cache_size=2600000-sample=0.10-leaves.png)

###curiosity

	if {age=Young,workclass=Private} then predict 1
	else if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
	else if {education=Bachelors,marital.status=Married} then predict 0
	else predict 1

![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2600000-sample=0.10-log](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2600000-sample=0.10-log.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2600000-sample=0.10-cache](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2600000-sample=0.10-cache.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2600000-sample=0.10-leaves](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=curiosity-max_cache_size=2600000-sample=0.10-leaves.png)

###lower_bound

	if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
	else if {occupation=Prof-specialty,relationship=Husband} then predict 0
	else if {marital.status=Married,occupation=Exec-managerial} then predict 0
	else predict 1

![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=lower_bound-max_cache_size=2600000-sample=0.10-log](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=lower_bound-max_cache_size=2600000-sample=0.10-log.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=lower_bound-max_cache_size=2600000-sample=0.10-cache](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=lower_bound-max_cache_size=2600000-sample=0.10-cache.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=lower_bound-max_cache_size=2600000-sample=0.10-leaves](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=lower_bound-max_cache_size=2600000-sample=0.10-leaves.png)


###objective

	if {capital.gain=7298LessThancapital-gain,capital.loss=capital-lossEQ0} then predict 0
	else if {marital.status=Married,occupation=Prof-specialty} then predict 0
	else if {marital.status=Married,occupation=Exec-managerial} then predict 0
	else predict 1

![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=objective-max_cache_size=2600000-sample=0.10-log](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=objective-max_cache_size=2600000-sample=0.10-log.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=objective-max_cache_size=2600000-sample=0.10-cache](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=objective-max_cache_size=2600000-sample=0.10-cache.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=objective-max_cache_size=2600000-sample=0.10-leaves](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=1.000-method=objective-max_cache_size=2600000-sample=0.10-leaves.png)

###random (start from min_objective = 0.201)

![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=0.201-method=random-max_cache_size=2600000-sample=0.10-log](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=0.201-method=random-max_cache_size=2600000-sample=0.10-log.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=0.201-method=random-max_cache_size=2600000-sample=0.10-cache](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=0.201-method=random-max_cache_size=2600000-sample=0.10-cache.png)
![adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=0.201-method=random-max_cache_size=2600000-sample=0.10-leaves](../figs/adult_R-serial_priority-c=0.01000-min_cap=0.010-min_objective=0.201-method=random-max_cache_size=2600000-sample=0.10-leaves.png)
