## summary

The last column reports the number of rules mined for (max cardinality, min support)

| dataset | # data | # 0 | # 1 | f. 0 | f. 1 | # dim | (2, 0.01) | done |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bcancer | 683 | 444 | 239 | 0.65 | 0.35 | 28 | 1,336 | yes |
| cars | 1,728 | 1,210 | 518 | 0.70 | 0.30 | 22 | 792 | no |
| haberman | 306 | 81 | 225 | 0.26 | 0.74 | 16 | 334 | yes |
| monks1 | 432 | 216 | 216 | 0.5 | 0.5 | 18 | 396 | yes |
| monks2 | 432 | 290 | 142 | 0.67 | 0.33 | 18 | 396 | no |
| monks3 | 432 | 204 | 228 | 0.47 | 0.53 | 18 | 396 | yes |
| votes | 435 | 168 | 267 | 0.39 | 0.61 | 17 | 512 | yes |
| adult | 30,081 | 7,436 | 22,645 | 0.25 | 0.75 | no |
| compas | 7,214 | 3,743 | 3,471 | 0.52 | 0.48 | 30 | 1,037 | yes |
| telco | 7,043 | 5,174 | 1,869 | 0.73 | 0.27 | 19 | 957 | no |

## [adult](https://archive.ics.uci.edu/ml/datasets/Adult)

**n = 48842 -> 30081 (Due to missing values?)**

**Redo rule mining for adult from original dataset**

| Probability for the label '>50K'  : 23.93% / 24.78% (without unknowns)
| Probability for the label '<=50K' : 76.07% / 75.22% (without unknowns)

1. age: continuous. 
2. workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked. 
3. fnlwgt: continuous. 
4. education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool. 
5. education-num: continuous. 
6. marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse. 
7. occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces. 
8. relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried. 
9. race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black. 
10. sex: Female, Male. 
11. capital-gain: continuous. 
12. capital-loss: continuous. 
13. hours-per-week: continuous. 
14. native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
15. >50K, <=50K

## [bcancer](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Original%29)

**n = 699 -> 683 (Due to missing values?)**

## [cars](https://archive.ics.uci.edu/ml/datasets/Car+Evaluation)

**n = 1728**

**How were the class values binarized?**

[cars description](https://archive.ics.uci.edu/ml/machine-learning-databases/car/car.names)

| # | attribute | values | description |
| --- | --- | --- | --- |
| 1 | buying | v-high, high, med, low | buying price |
| 2 | maint | v-high, high, med, low | price of the maintenance |
| 3 | doors | 2, 3, 4, 5-more | number of doors |
| 4 | persons | 2, 4, more | capacity in terms of persons to carry |
| 5 | lug_boot | small, med, big | the size of luggage boot |
| 6 | safety | low, med, high| estimated safety of the car |
| 7 | class | unacc, acc, good, vgood | car evaluation |

## [haberman](https://archive.ics.uci.edu/ml/datasets/Haberman%27s+Survival) [(description)](https://archive.ics.uci.edu/ml/machine-learning-databases/haberman/haberman.names)

**n = 306**

1. Age of patient at time of operation (numerical) 
2. Patient's year of operation (year - 1900, numerical) 
3. Number of positive axillary nodes detected (numerical) 
4. Survival status (class attribute) 
-- 1 = the patient survived 5 years or longer 
-- 2 = the patient died within 5 year

## [monks](https://archive.ics.uci.edu/ml/datasets/MONK%27s+Problems) [(description)](https://archive.ics.uci.edu/ml/machine-learning-databases/monks-problems/monks.names)

**n = 432**

**See below: monks2 doesn't look like a good problem for us**

Attribute information:
    1. class: 0, 1 
    2. a1:    1, 2, 3
    3. a2:    1, 2, 3
    4. a3:    1, 2
    5. a4:    1, 2, 3
    6. a5:    1, 2, 3, 4
    7. a6:    1, 2
    8. Id:    (A unique symbol for each instance)

**MONK-1:** (a1 = a2) or (a5 = 1)

**MONK-2:** EXACTLY TWO of {a1 = 1, a2 = 1, a3 = 1, a4 = 1, a5 = 1, a6 = 1}

**MONK-3:** (a5 = 3 and a4 = 1) or (a5 /= 4 and a2 /= 3)
       (5% class noise added to the training set)

## [votes](https://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Records)

**n = 435**

**How are missing values handled?**

1. Class Name: 2 (democrat, republican) 
2. handicapped-infants: 2 (y,n) 
3. water-project-cost-sharing: 2 (y,n) 
4. adoption-of-the-budget-resolution: 2 (y,n) 
5. physician-fee-freeze: 2 (y,n) 
6. el-salvador-aid: 2 (y,n) 
7. religious-groups-in-schools: 2 (y,n) 
8. anti-satellite-test-ban: 2 (y,n) 
9. aid-to-nicaraguan-contras: 2 (y,n) 
10. mx-missile: 2 (y,n) 
11. immigration: 2 (y,n) 
12. synfuels-corporation-cutback: 2 (y,n) 
13. education-spending: 2 (y,n) 
14. superfund-right-to-sue: 2 (y,n) 
15. crime: 2 (y,n) 
16. duty-free-exports: 2 (y,n) 
17. export-administration-act-south-africa: 2 (y,n)

## [telco](https://www.ibm.com/communities/analytics/watson-analytics-blog/predictive-insights-in-the-telco-customer-churn-data-set/) [(download)](https://community.watsonanalytics.com/wp-content/uploads/2015/03/WA_Fn-UseC_-Telco-Customer-Churn.csv)

**n = 7043**

## IBM Watson Analytics sample data sets

[guide to sample datasets](https://www.ibm.com/communities/analytics/watson-analytics-blog/guide-to-sample-datasets/)

[list of datasets](https://www.ibm.com/communities/analytics/watson-analytics/resources/?r=dataset#resource-table)

## [bank marketing](https://archive.ics.uci.edu/ml/datasets/Bank+Marketing)

**n = 45211**
