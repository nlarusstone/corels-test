from collections import defaultdict,Counter
import os

from fim import fpgrowth #this is PyFIM, available from http://www.borgelt.net/pyfim.html
import numpy as np

#Read in the .tab file
def load_data(fname):
    #Load data
    with open(fname+'.tab','r') as fin:
        A = fin.readlines()
    data = []
    for ln in A:
        data.append(ln.split())
    #Now load Y
    Y = np.loadtxt(fname+'.Y')
    if len(Y.shape)==1:
        Y = np.array([Y])
    return data,Y

#Frequent itemset mining
def get_freqitemsets(fname,minsupport,maxlhs):
    #minsupport is an integer percentage (e.g. 10 for 10%)
    #maxlhs is the maximum size of the lhs
    #first load the data
    data,Y = load_data(fname)
    #Now find frequent itemsets
    #Mine separately for each class
    data_pos = [x for i,x in enumerate(data) if Y[i,0]==0]
    data_neg = [x for i,x in enumerate(data) if Y[i,0]==1]
    assert len(data_pos)+len(data_neg) == len(data)
    try:
        itemsets = [r[0] for r in fpgrowth(data_pos,supp=minsupport,zmax=maxlhs)]
        itemsets.extend([r[0] for r in fpgrowth(data_neg,supp=minsupport,zmax=maxlhs)])
    except TypeError:
        itemsets = [r[0] for r in fpgrowth(data_pos,supp=minsupport,max=maxlhs)]
        itemsets.extend([r[0] for r in fpgrowth(data_neg,supp=minsupport,max=maxlhs)])
    itemsets = list(set(itemsets))
    print len(itemsets),'rules mined'
    #Now form the data-vs.-lhs set
    #X[j] is the set of data points that contain itemset j (that is, satisfy rule j)
    X = [ set() for j in range(len(itemsets)+1)]
    X[0] = set(range(len(data))) #the default rule satisfies all data
    for (j,lhs) in enumerate(itemsets):
        X[j+1] = set([i for (i,xi) in enumerate(data) if set(lhs).issubset(xi)])
    #now form lhs_len
    lhs_len = [0]
    for lhs in itemsets:
        lhs_len.append(len(lhs))
    nruleslen = Counter(lhs_len)
    lhs_len = np.array(lhs_len)
    itemsets_all = ['null']
    itemsets_all.extend(itemsets)
    return X,Y,nruleslen,lhs_len,itemsets_all

def array_to_string(x):
    return list(x).__repr__().replace(',', '').strip('[]')

def titanic(din='../data/titanic', dout='../data/titanic'):
    froot = 'titanic'

    #rule mining parameters
    maxlhs = 2 #maximum cardinality of an itemset
    minsupport = 10 #minimum support (%) of an itemset

    #Do frequent itemset mining from the training data
    fname = os.path.join(din, froot+'_train')
    Xtrain,Ytrain,nruleslen,lhs_len,itemsets = get_freqitemsets(fname,minsupport,maxlhs)

    nrules = len(Xtrain)
    ndata = len(Xtrain[0])
    out = []
    for i in range(1, nrules):
        ind = list(Xtrain[i])
        ind.sort()
        row = np.zeros(ndata, int)
        row[ind] = 1
        rule_name = '{%s}' % ','.join(itemsets[i])
        rule_repr = array_to_string(row)
        out += [' '.join([rule_name, rule_repr])]

    label = [' '.join(('{label=0}', array_to_string(np.cast[int](Ytrain[:,0]))))]
    label += [' '.join(('{label=1}', array_to_string(1 - np.cast[int](Ytrain[:,0]))))]

    fout = os.path.join(dout, '%s.out' % froot)
    f = open(fout, 'w')
    f.write('\n'.join(out))
    f.close()

    flabel = os.path.join(dout, '%s.label' % froot)
    f = open(flabel, 'w')
    f.write('\n'.join(label))
    f.close()
    return
