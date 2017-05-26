"""
See https://archive.ics.uci.edu/ml/datasets/Diabetes+130-US+hospitals+for+years+1999-2008

Original paper: https://www.hindawi.com/journals/bmri/2014/781670/

On primary diagnosis: https://www.hindawi.com/journals/bmri/2014/781670/tab2/

Variables:  https://www.hindawi.com/journals/bmri/2014/781670/tab3/

"To summarize, our dataset consists of hospital admissions of length between one
and 14 days that did not result in a patient death or discharge to a hospice.
Each encounter corresponds to a unique patient diagnosed with diabetes, although
the primary diagnosis may be different. During each of the analyzed encounters,
lab tests were ordered and medication was administered."  => N = 69,984

101,766 records
71,518 unique patients

"readmitted" ?
54,864 records say "NO" (54%)
35,545 records say ">30" (readmitted after 30 days)
11,357 records say "<30" (readmitted within 30 days)

* descriptions of 3 coded attributes in IDs_mapping.csv

race 6 {'?', 'AfricanAmerican', 'Asian', 'Caucasian', 'Hispanic', 'Other'} (group together ? = 2.2% and Other = 1.5%)
gender 3 {'Female', 'Male', 'Unknown/Invalid'} ('Unknown/Invalid' = 3 records)
age 10 {'[0-10)', '[10-20)', ..., '[90-100)'}
    (group together 0-30 = 2.5%; 0-40 = 6%, 0-50 = 16%, 0-60 = 30%, 60-70 = 22%, 70-80 = 26%, 80-100 = 20%)
weight 10 { '?', '[0-25)', '[25-50)', ..., '[175-200)', '>200'} (? = 97%) => IGNORE
*admission_type_id 8 {1, 2, 3, 4, 5, 6, 7, 8}
    1,Emergency (53%), 2,Urgent (18%), 3,Elective (18%)
    4,Newborn (10 total), 5,Not Available, 6,NULL, 7,Trauma Center (21 total), 8,Not Mapped => GROUP
*discharge_disposition_id 26 {1, 2, ..., 28} - {21, 26}
    => group 11, 19-21 (Expired, 2%); group 18, 25 (Null/Not mapped, 5%); group if contains "discharged", excluding 1
    1,Discharged to home (59%)
    2,Discharged/transferred to another short term hospital (2%)
    3,Discharged/transferred to SNF (14%)
    4,Discharged/transferred to ICF (0.8%)
    5,Discharged/transferred to another type of inpatient care institution (1%)
    6,Discharged/transferred to home with home health service (13%)
    7,Left AMA (0.6%)
    8,Discharged/transferred to home under care of Home IV provider (0.1%)
    9,Admitted as an inpatient to this hospital (0.02%)
    10,Neonate discharged to another hospital for neonatal aftercare (0.005%)
    11,Expired (1.6%)                                                       => DISCARD EXPIRED PATIENTS
    12,Still patient or expected to return for outpatient services (0.003%)
    13,Hospice / home (0.4%)
    14,Hospice / medical facility (0.4%)
    15,Discharged/transferred within this institution to Medicare approved swing bed (0.06%)
    16,Discharged/transferred/referred another institution for outpatient services (0.01%)
    17,Discharged/transferred/referred to this institution for outpatient services (0.01%)
    18,NULL (4%)
    19,"Expired at home. Medicaid only, hospice." (0.008%)                  => DISCARD EXPIRED PATIENTS
    20,"Expired in a medical facility. Medicaid only, hospice." (0.002%)    => DISCARD EXPIRED PATIENTS
    21,"Expired, place unknown. Medicaid only, hospice." (0%)               => DISCARD EXPIRED PATIENTS
    22,Discharged/transferred to another rehab fac including rehab units of a hospital. (2%)
    23,Discharged/transferred to a long term care hospital. (0.4%)
    24,Discharged/transferred to a nursing facility certified under Medicaid but not certified under Medicare. (0.04%)
    25,Not Mapped (1%)
    26,Unknown/Invalid (0%)
    27,Discharged/transferred to a federal health care facility. (0.004%)
    28,Discharged/transferred/referred to a psychiatric hospital of psychiatric distinct part unit of a hospital (0.1%)
    29,Discharged/transferred to a Critical Access Hospital (CAH) (0%)
    30,Discharged/transferred to another Type of Health Care Institution not Defined Elsewhere (0%)
*admission_source_id 17 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 17, 20, 22, 25}
    => 1 = physician referral, 1-3 = referral, 4 = transfer from hospital, 4-6, 25 = transfer from health care facility (5%)
    => 7 = ER, 17, 20 = NULL/Not Mapped, Other
    1, Physician Referral (30%)
    2,Clinic Referral (1%)
    3,HMO Referral (0.2%)
    4,Transfer from a hospital (3%)
    5, Transfer from a Skilled Nursing Facility (SNF) (0.8%)
    6, Transfer from another health care facility (2.2%)
    7, Emergency Room (56%)
    8, Court/Law Enforcement (0.02%)
    9, Not Available (0.1%)
    10, Transfer from critial access hospital (0.007%)
    11,Normal Delivery (0.001%)
    12, Premature Delivery (0%)
    13, Sick Baby (0.001%)
    14, Extramural Birth (0.002%)
    15,Not Available (0%)
    17,NULL (7%)
    18, Transfer From Another Home Health Agency (0%)
    19,Readmission to Same Home Health Agency (0%)
    20, Not Mapped (0.2%)
    21,Unknown/Invalid (0%)
    22, Transfer from hospital inpt/same fac reslt in a sep claim (0.01%)
    23, Born inside this hospital (0%)
    24, Born outside this hospital (0%)
    25, Transfer from Ambulatory Surgery Center (0.002%)
    26,Transfer from Hospice (0%)
time_in_hospital 14 {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14} (quartiles: [1, 2, 4, 6, 14])
payer_code 18 {'?', 'BC', 'CH', 'CM', 'CP', 'DM', 'FR', 'HM', ...} (? = 40%) => IGNORE
medical_specialty 73 {'?', 'AllergyandImmunology', 'Anesthesiology', 'Anesthesiology-Pediatric', ...} (? = 49%)
num_lab_procedures 118 {1, ..., 132} (quartiles: [1, 31, 44, 57, 132])
num_procedures 7 {0, 1, 2, 3, 4, 5, 6} (quartiles: [0, 0, 1, 2, 6])
num_medications 75 {1, ..., 81} (quartiles: [1, 10, 15, 20, 81])
number_outpatient 39 {0, ..., 42} (0 = 84%, 1 = 8%, >1 = 8%)
number_emergency 33 {0, ..., 76} (0 = 89%, 1 = 8%, >1 = 4%)
number_inpatient 21 {0, ..., 21} (0 = 66%, 1 = 19%, >1 = 14%)
diag_1 717 ... 916 distinct diagnoses => IGNORE for now but look for diagnoses with significant support
diag_2 749
diag_3 790
number_diagnoses 16 {1, ..., 16} (quartiles: [1, 6, 8, 9, 16]) (1-5 = 21%, 6-8 = 30%, 9 = 49%, >=9 = 49%)
max_glu_serum 4 {'>200', '>300', 'None', 'Norm'} (1.5%, 1.2%, 95%, 2.6%) => 200-300, >300, >200 OR >300 (call this > 200)
A1Cresult 4 {'>7', '>8', 'None', 'Norm'}
metformin 4 {'Down', 'No', 'Steady', 'Up'} (4%, 8%, 83%, 5%)
repaglinide 4 {'Down', 'No', 'Steady', 'Up'}
nateglinide 4 {'Down', 'No', 'Steady', 'Up'}
chlorpropamide 4 {'Down', 'No', 'Steady', 'Up'}
glimepiride 4 {'Down', 'No', 'Steady', 'Up'}
acetohexamide 2 {'No', 'Steady'}
glipizide 4 {'Down', 'No', 'Steady', 'Up'}
glyburide 4 {'Down', 'No', 'Steady', 'Up'}
tolbutamide 2 {'No', 'Steady'}
pioglitazone 4 {'Down', 'No', 'Steady', 'Up'}
rosiglitazone 4 {'Down', 'No', 'Steady', 'Up'}
acarbose 4 {'Down', 'No', 'Steady', 'Up'}
miglitol 4 {'Down', 'No', 'Steady', 'Up'}
troglitazone 2 {'No', 'Steady'}
tolazamide 3 {'No', 'Steady', 'Up'}
examide 1 {'No'} => IGNORE
citoglipton 1 {'No'} => IGNORE
insulin 4 {'Down', 'No', 'Steady', 'Up'}
glyburide-metformin 4 {'Down', 'No', 'Steady', 'Up'}
glipizide-metformin 2 {'No', 'Steady'}
glimepiride-pioglitazone 2 {'No', 'Steady'}
metformin-rosiglitazone 2 {'No', 'Steady'}
metformin-pioglitazone 2 {'No', 'Steady'}
change 2 {'Ch', 'No'}
diabetesMed 2 {'No', 'Yes'}
readmitted 3 {'<30', '>30', 'NO'} (11%, 35%, 54%)

"""
import os

import numpy as np
import tabular as tb

import mine
import utils


def add_columns(tab, cols, names):
    return tab.colstack(tb.tabarray(columns=columns, names=names))

def chunk_to_dict(c):
    return dict([(int(i.split(',')[0]), i.split(',')[1].strip()) for i in c.split('\n')[1:]])

def race_func(a):
    if (a in ['AfricanAmerican', 'Caucasian']):
        return a
    elif (a == '?'):
        return 'Missing'
    else:
        return 'Other'

def age_func(a):
    if (a in ['[0-10)', '[10-20)', '[20-30)']):
        return '<30'
    elif (a in ['[30-40)', '[40-50)', '[50-60)']):
        return '30-60'
    else:
        return '>=60'

def discharge_func(a):
    if (a == 1):
        return 'Discharged-to-home'
    else:
        return 'Otherwise'

def admission_source_func(a):
    if (a in [1, 2]):
        return 'Physician-or-clinic-referral'
    elif (a == 7):
        return 'Emergency-room'
    else:
        return 'Otherwise'

def medical_specialty_func(a):
    if (a in ['InternalMedicine', 'Family/GeneralPractice']):
        return a
    elif (a == '?'):
        return 'Missing-or-unknown'
    elif (a in ['Cardiology', 'Cardiology-Pediatric']):
        return 'Cardiology'
    elif (a in ['Surgery-General', 'Surgery-Cardiovascular/Thoracic', 'Surgery-Neuro', 'Surgery-Vascular', 'Surgery-Cardiovascular']):
        return 'Surgery'
    else:
        return 'Other'

def primary_diagnosis_func(a):
    if (a.startswith('250')):
        return 'Diabetes'
    elif (a.isdigit()):
        a = int(a)
        if (((a >= 390) and (a <= 459)) or (a == 785)):
            return 'Circulatory-system-disease'
        elif (((a >= 460) and (a <= 519)) or (a == 786)):
            return 'Respiratory-system-disease'
        elif (((a >=520) and (a <= 579)) or (a == 787)):
            return 'Digestive-system-diseases'
        elif ((a >= 800) and (a <= 999)):
            return 'Injury-and-poisoning'
        elif ((a >= 710) and (a <= 739)):
            return 'Musculoskeletal-system-and-connective-tissue-diseases'
        elif (((a >= 580) and (a <= 629)) or (a == 788)):
            return 'Genitourinary-system-diseases'
        elif ((a >= 140) and (a <= 239)):
            return 'Neoplasms'
        else:
            return 'Other'
    else:
        return 'Other'

def quartiles_func(a, q):
    if (a <= q[1]):
        return ('%d-%d' % (q[0], q[1]))
    elif (a <= q[2]):
        return ('%d-%d' % (q[1] + 1, q[2]))
    elif (a <= q[3]):
        return ('%d-%d' % (q[2] + 1, q[3]))
    else:
        return ('%d-%d' % (q[3] + 1, q[4]))

def quartiles(col):
    q = np.percentile(col, [0, 25, 50, 75, 100])
    return np.array([quartiles_func(a, q) for a in col])


seed = 65
num_folds = 10
max_cardinality = 2
min_support = 0.01
prefix = ''

labels = ['<30', 'Other']
minor = True

din = os.path.join('..', 'data', 'diabetes')
dout = os.path.join('..', 'data', 'CrossValidation')
zin = os.path.join(din, 'dataset_diabetes.zip')
zout = os.path.join(din, 'dataset_diabetes')
fin = os.path.join(zout, 'diabetic_data.csv')
fmap = os.path.join(zout, 'IDs_mapping.csv')
fout = os.path.join(din, 'hospital.csv')
bout = os.path.join(din, 'hospital-binary.csv')

if not os.path.exists(din):
    os.mkdir(din)

if not os.path.exists(fin):
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00296/dataset_diabetes.zip'
    os.system('wget %s -O %s' % (url, zin))
    os.system('unzip %s -d %s' % (zin, din))

x = tb.tabarray(SVfile=fin)

"""
"... we considered only the first encounter for each patient as the primary
admission and determined whether or not they were readmitted within 30 days.
Additionally, we removed all encounters that resulted in either discharge to a
hospice or patient death, to avoid biasing our analysis. After performing the
above-described operations, we were left with 69,984 encounters that constituted
the final dataset for analysis."

"""
print 'original # records:', len(x) # 101,766
unique_ids = set()
bvec = np.zeros(len(x), bool)
for (i, rec) in enumerate(x):
    if (rec['patient_nbr'] in unique_ids):
        continue
    else:
        unique_ids.add(rec['patient_nbr'])
        bvec[i] = True

print '# records after taking only first patient encounters', bvec.sum() # 71,518
x = x[bvec]

"""
11,Expired (1.6%)
13,Hospice / home (0.4%)
14,Hospice / medical facility (0.4%)
19,"Expired at home. Medicaid only, hospice." (0.008%)
20,"Expired in a medical facility. Medicaid only, hospice." (0.002%)
21,"Expired, place unknown. Medicaid only, hospice." (0%)
"""
bvec = np.array([False if a in [11, 13, 14, 19, 20, 21] else True for a in x['discharge_disposition_id']])

print '# records after filtering w.r.t. hospice or death', bvec.sum() # 69,973
x = x[bvec]

# readmitted 3 {'<30', '>30', 'NO'} (11%, 35%, 54%)
y = tb.tabarray(columns=[[1 if (r == '<30') else 0 for r in x['readmitted']]], names='readmitted')

z = open(fmap, 'rU').read().strip().split('\n,\n')
admission_dict = chunk_to_dict(z[0])
discharge_dict = chunk_to_dict(z[1])
admission_source_dict = chunk_to_dict(z[2])

# skip: encounter_id, patient_nbr, weight (97% marked ?), payer_code

print 'demographics'
# use as is:  gender

#race 6 {'?', 'AfricanAmerican', 'Asian', 'Caucasian', 'Hispanic', 'Other'} (group together ? = 2.2% and Other = 1.5%)
race = [race_func(a) for a in x['race']]

# age (group together 0-30 = 2.5%; 0-40 = 6%, 0-50 = 16%, 0-60 = 30%, 60-70 = 22%, 70-80 = 26%, 80-100 = 20%)
age = [age_func(a) for a in x['age']]

columns = [x['gender'], race, age]
names = ['gender', 'race', 'age']
categorical = tb.tabarray(columns=columns, names=names)

print 'admission/discharge info'
# see IDs_mapping.csv
discharge_disposition = [discharge_func(a) for a in x['discharge_disposition_id']]
admission_source = [admission_source_func(a) for a in x['admission_source_id']]

columns = [discharge_disposition, admission_source]
names = ['discharge_disposition', 'admission_source']
categorical = add_columns(categorical, columns, names)

print 'patient info'
# quartiles
time_in_hospital = quartiles(x['time_in_hospital'])

columns = [time_in_hospital]
names = ['time_in_hospital']
categorical = add_columns(categorical, columns, names)

print 'medical specialty' # specialty of the admitting physician
# medical_specialty 73 {'?', 'AllergyandImmunology', 'Anesthesiology', 'Anesthesiology-Pediatric', ...} (? = 49%)
specialty = [medical_specialty_func(a) for a in x['medical_specialty']]

columns = [specialty]
names = ['specialty']
categorical = add_columns(categorical, columns, names)

print 'diagnoses'
# 916 distinct diagnoses => look for diagnoses with significant support
# diag_1 717, diag_2 749, diag_3 790
primary_diagnosis = [primary_diagnosis_func(a) for a in x['diag_1']]

columns = [primary_diagnosis]
names = ['primary_diagnosis']
categorical = add_columns(categorical, columns, names)

print 'drugs/lab tests'
# A1Cresult 4 {'>7', '>8', 'None', 'Norm'} (4%, 8%, 83%, 5%)
# change 2 {'Ch', 'No'}
# diabetesMed 2 {'No', 'Yes'}
HbA1c_no_test = np.cast[str](x['A1Cresult'] == 'None')
bvec = (x['A1Cresult'] == '>8') & (x['diabetesMed'] == 'Yes') & (x['change'] == 'Ch')
HbA1c_high_changed = np.cast[str](bvec)
bvec = (x['A1Cresult'] == '>8') & (x['diabetesMed'] == 'Yes') & (x['change'] == 'No')
HbA1c_high_not_changed = np.cast[str](bvec)
HbA1c_normal_test = np.cast[str](x['A1Cresult'] == 'Norm')

columns = [HbA1c_no_test, HbA1c_high_changed, HbA1c_high_not_changed, HbA1c_normal_test]
names = ['HbA1c-no-test', 'HbA1c-result-high-diabetic-medication-changed', 'HbA1c-result-high-diabetic-medication-not-changed', 'HbA1c-normal-test']
categorical = add_columns(categorical, columns, names)

x = categorical.colstack(y)

print 'write categorical dataset', fout
x.saveSV(fout)

print 'write binary dataset', bout
b = utils.to_binary(x)
b.saveSV(bout)

y0 = x[x['readmitted'] == 0]
y1 = x[x['readmitted'] == 1]
x = y0.rowstack(y1)
s0 = np.split(np.random.permutation(len(y0) / num_folds * num_folds), num_folds)
s1 = np.split(len(y0) + np.random.permutation(len(y1) / num_folds * num_folds), num_folds)
s1 = [i1[np.random.randint(0, len(i1), len(s0[0]))] for i1 in s1]
split_ind = [np.concatenate([i0, i1]) for (i0, i1) in zip(s0, s1)]

print 'permute and partition dataset'
print 'number of folds:', num_folds
print 'train size:', len(split_ind[0]) * (num_folds - 1) # 114,642
print 'test size:', len(split_ind[0]) # 12,738

num_rules = np.zeros(num_folds, int)
for i in range(num_folds):
    print 'generate cross-validation split', i
    cv_root = 'hospital_%d' % i
    test_root = '%s_test' % cv_root
    train_root = '%s_train' % cv_root
    ftest = os.path.join(dout, '%s.csv' % test_root)
    ftrain = os.path.join(dout, '%s.csv' % train_root)
    btest = os.path.join(dout, '%s-binary.csv' % test_root)
    btrain = os.path.join(dout, '%s-binary.csv' % train_root)
    train_ind = np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)])
    x[split_ind[i]].saveSV(ftest)
    x[train_ind].saveSV(ftrain)
    b[split_ind[i]].saveSV(btest)
    b[train_ind].saveSV(btrain)
    print 'mine rules from', ftrain
    num_rules[i] = mine.mine_rules(din=dout, froot=train_root,
                                   max_cardinality=max_cardinality,
                                   min_support=min_support, labels=labels,
                                   minor=minor, prefix=prefix)
    mine.apply_rules(din=dout, froot=cv_root, labels=labels, prefix=prefix)

print '(min, max) # rules mined per fold:', (num_rules.min(), num_rules.max())
