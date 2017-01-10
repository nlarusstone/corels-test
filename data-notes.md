## summary

The last column reports the number of rules mined for (max cardinality, min support)

| name | # data | # 0 | # 1 | f. 0 | f. 1 | d | 2, .01 | note | 3, .01 | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bcancer | 683 | 444 | 239 | 0.65 | 0.35 | 27 | 1,336 | done | 16,365 | - |
| cars | 1,728 | 1,210 | 518 | 0.70 | 0.30 | 21 | 792 | **no** | - | - |
| haberman | 306 | 81 | 225 | 0.26 | 0.74 | 15 | 334 | done | - | - |
| monks1 | 432 | 216 | 216 | 0.5 | 0.5 | 17 | 396 | yes | n/a | n/a |
| monks2 | 432 | 290 | 142 | 0.67 | 0.33 | 17 | 396 | n/a | 2,720 | **semi** |
| monks3 | 432 | 204 | 228 | 0.47 | 0.53 | 17 | 396 | yes | n/a | n/a |
| votes | 435 | 168 | 267 | 0.39 | 0.61 | 16 | 512 | yes | - | - |
| adult | 30,081 | 7,436 | 22,645 | 0.25 | 0.75 | ? | 283 | **no** | - | - |
| compas | 7,214 | 3,743 | 3,471 | 0.52 | 0.48 | 30 | 1,037 | yes | 10,209 | - |
| telco | 7,043 | 5,174 | 1,869 | 0.73 | 0.27 | 19 | 957 | **no** | - | - |
| tdata | - | - | - | - | - | - | n/a | n/a | - | - |

## [tdata](https://archive.ics.uci.edu/ml/datasets/Tic-Tac-Toe+Endgame)

**n = 958 -> 639**

**Redo rule mining for tdata if we're including it**

## [adult](https://archive.ics.uci.edu/ml/datasets/Adult)

**n = 30162 -> 30081 (Due to missing values?)**

* `adult.data` n = 30162 after excluding records containing `?`

**Redo rule mining for adult from original dataset?**

`fnlweight` represents "the # of people the census takers believe that observation represents"
(see http://scg.sdsu.edu/dataset-adult_r/) -- is this safe to ignore?

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

age=Middle-aged, age=Senior, age=Young
capital.gain=7298LessThancapital-gain, capital.gain=capital-gainEQ0, capital.loss=capital-lossEQ0
education=Assoc-degree, education=Bachelors, education=Grad-school, education=HS-grad, education=Some-college, education=Some-high-school
hours.per.week=Full-time, hours.per.week=Over-time, hours.per.week=Part-time
marital.status=Married, marital.status=Never-married, marital.status=Not-married-anymore
native.country=N-America
occupation=Adm-clerical, occupation=Craft-repair, occupation=Exec-managerial, occupation=Other-service, occupation=Prof-specialty, occupation=Sales
race=Black, race=White
relationship=Husband, relationship=Not-in-family, relationship=Own-child, relationship=Unmarried
sex=Female, sex=Male
workclass=Gov, workclass=Private, workclass=Self-emp

## compas

**Why are we excluding the following?**

* c_charge_degree: M or F (misdemeanor charge, felony charge?)
* juv_misd_count
* juv_other_count
* is_recid
* r_charge_degree: (F5), (MO3), (M1), (F6), (M2), (F1), (F2), (F3), (CO3), (F7)
* is_violent_recid

Attributes:

Age<=18, Age=18-22, Age<=20, Age<=22, Age<=25, Age=24-30, Age=24-40, Age>=30, Age<=40, Age<=45

Gender=Male

Race=African-American, Race=Caucasian, Race=Asian, Race=Hispanic, Race=Native_American, Race=Other

Juvenile_Felonies=0, Juvenile_Felonies=1-3, Juvenile_Felonies>=3, Juvenile_Felonies>=5

Juvenile_Crimes=0, Juvenile_Crimes=1-3, Juvenile_Crimes>=3, Juvenile_Crimes>=5

Prior_Crimes=0, Prior_Crimes=1-3, Prior_Crimes>=3, Prior_Crimes>=5

## [bcancer](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Original%29)

**n = 699 -> 683 (excludes 16 records containing missing values)**

1. Sample code number: id number
2. Clump Thickness (a1): 1 - 10
3. Uniformity of Cell Size (a2): 1 - 10
4. Uniformity of Cell Shape (a3): 1 - 10
5. Marginal Adhesion (a4): 1 - 10
6. Single Epithelial Cell Size (a5): 1 - 10
7. Bare Nuclei (a6): 1 - 10
8. Bland Chromatin (a7): 1 - 10
9. Normal Nucleoli (a8): 1 - 10
10. Mitoses (a9): 1 - 10
11. Class: (2 for benign, 4 for malignant)

a1<5, a1.5-7, a1>7

a2<5, a2.5-7, a2>7

a3<5, a3.5-7, a3>7

a4<5, a4.5-7, a4>7

a5<5, a5.5-7, a5>7

a6<5, a6.5-7, a6>7

a7<5, a7.5-7, a7>7

a8<5, a8.5-7, a8>7

a9<5, a9.5-7, a9>7

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

buying=vhigh, buying=high, buying=med, buying=low, maint=vhigh

maint=high, maint=med, maint=low

doors=2, doors=3, doors=4, doors=5more

persons=2, persons=4, persons=more

lug-boot=small, lug-boot=med, lug-boot=big

safety=low, safety=med, safety=high

## [haberman](https://archive.ics.uci.edu/ml/datasets/Haberman%27s+Survival) [(description)](https://archive.ics.uci.edu/ml/machine-learning-databases/haberman/haberman.names)

**n = 306**

1. Age of patient at time of operation (numerical) 
2. Patient's year of operation (year - 1900, numerical) 
3. Number of positive axillary nodes detected (numerical) 
4. Survival status (class attribute) 
-- 1 = the patient survived 5 years or longer 
-- 2 = the patient died within 5 year

age<40, age40-49, age50-59, age60-69, age>69

year<60, year60-61, year62-63, year64-65, year>65

nodes0, nodes1-9, nodes10-19, nodes20-29, nodes>29

## [monks](https://archive.ics.uci.edu/ml/datasets/MONK%27s+Problems) [(description)](https://archive.ics.uci.edu/ml/machine-learning-databases/monks-problems/monks.names)

**n = 432**

**See below:** monks2 looks like it needs at least 3 clauses and also should use
small regularization because there are many specific conditions

e.g., using c = 0.001 quickly finds a perfect rule list of length 30

    ./bbcache -c 1 -p 1 -r 0.001 -n 1000000 ../data/monks2-3.out ../data/monks2-3.label

Attribute information:
    1. class: 0, 1 
    2. a1:    1, 2, 3
    3. a2:    1, 2, 3
    4. a3:    1, 2
    5. a4:    1, 2, 3
    6. a5:    1, 2, 3, 4
    7. a6:    1, 2
    8. Id:    (A unique symbol for each instance)

a1=1, a1=2, a1=3
a2=1, a2=2, a2=3
a3=1, a3=2
a4=1, a4=2, a4=3
a5=1, a5=2, a5=3, a5=4
a6=1, a6=2

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

## [diabetes-130](https://archive.ics.uci.edu/ml/datasets/Diabetes+130-US+hospitals+for+years+1999-2008)

**n = 100000**

Hospital readmission for diabetes patients (contains missing data but good)

Predict readmission within 30 days (or alternatively, readmission anytime)

## [census-income (kdd)](https://archive.ics.uci.edu/ml/datasets/Census-Income+%28KDD%29)

**n = 299285**

**Weighted** census data with missing values
