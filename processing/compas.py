"""
Age<=18,Age=18-22,Age<=20,Age<=22,Age<=25,Age=24-30,Age=24-40,Age>=30,Age<=40,Age<=45,Gender=Male,Race=African-American,Race=Caucasian,Race=Asian,Race=Hispanic,Race=Native_American,Race=Other,Juvenile_Felonies=0,Juvenile_Felonies=1-3,Juvenile_Felonies>=3,Juvenile_Felonies>=5,Juvenile_Crimes=0,Juvenile_Crimes=1-3,Juvenile_Crimes>=3,Juvenile_Crimes>=5,Prior_Crimes=0,Prior_Crimes=1-3,Prior_Crimes>=3,Prior_Crimes>=5,y

"""
import tabular as tb

def age_func(a):
    if (a <= 20):       # minimum age is 18
        return '18-20'  # support = 220
    elif (a <= 22):
        return '21-25'  # support = 1641
    elif (a <= 25):
        return '26-30'  # support = 1512
    elif (a <= 40):
        return '31-40'  # support = 1818
    elif (a <= 50):
        return '41-50'  # support = 1045
    elif (a <= 60):
        return '51-60'  # support = 748
    else:
        return '>60'    # support = 230

def priors_count_func(p):
    if (p == 0):
        return '=0'     # support = 2150
    elif (p <= 1):
        return '=1'     # support = 1397
    elif (p <= 3):
        return '2-3'    # support = 1408
    elif (p <= 9):
        return '4-9'    # support = 1523
    else:
        return '>=10'   # support = 736

fin = '../compas/compas-scores-two-years.csv'

x = tb.tabarray(SVfile=fin)

# duplicate names in header:  decile_score, priors_count
names = open(fin, 'rU').read().strip().split('\n')[0].split(',')

nlist = []
for (d, n) in zip(x.dtype.names, names):
    if n in nlist:
        print 'duplicate name', n, '->', n + '_'
        x.renamecol(d, '%s_' % n)
    else:
        x.renamecol(d, n)
        nlist.append(n)

assert (x['priors_count'] == x['priors_count_']).all()
assert (x['decile_score'] == x['decile_score_']).all()

"""
columns = [(x['sex'] == 'Male'),
           (x['age'] <= 20), (x['age'] <= 22), (x['age'] <= 25),
           (x['age'] < 30), (x['age'] >= 60),
           ((x['age'] >= 30) & (x['age'] <= 44)),
           ((x['age'] >= 45) & (x['age'] <= 59))]
"""

age = np.array([age_func(i) for i in x['age']])

juvenile_felonies = np.array(['>0' if (i > 0) else '=0' for i in x['juv_fel_count']])   # support = 282

juvenile_misdemeanors = np.array(['>0' if (i > 0) else '=0' for i in x['juv_misd_count']])  # support = 415

priors_count = np.array([priors_count_func(i) for i in x['priors']])

columns = [x['sex'], age, juvenile_felonies, juvenile_misdemeanors]

cnames = ['age', 'sex', 'juvenile-felonies', 'juvenile_misdemeanors', 'priors']

"""
race_list = list(set(x['race']))
 
columns += [(x['race'] == n) for n in race_list]

cnames = ['Gender=Male', 'Age=18-20', 'Age=18-22', 'Age=18-25',
          'Age<30', 'Age>=60', 'Age=30-44', 'Age=45-59']

cnames += ['Race=%s' % r for r in race_list]
"""

y = tb.tabarray(columns=columns, names=cnames)

