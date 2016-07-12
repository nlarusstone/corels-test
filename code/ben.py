from collections import defaultdict,Counter
import os

from fim import fpgrowth #this is PyFIM, available from http://www.borgelt.net/pyfim.html
import numpy as np


#Read in the .tab file
def load_data(fname, yname=None, header=False, delimiter=' '):
    #Load data
    with open(fname,'r') as fin:
        A = fin.readlines()
    if header:
        colnames = A[0].split(delimiter)
        A = A[1:]
    data = []
    for ln in A:
        data.append(ln.split(delimiter))
    #Now load Y
    if (yname is None):
        Y = 1 - np.array([int(d[-1]) for d in data])
        data = [d[:-1] for d in data]
    else:
        Y = np.loadtxt(yname)
    if len(Y.shape)==1:
        Y = Y.reshape((len(Y), 1))
    if header:
        return data,Y,colnames
    else:
        return data,Y

#Frequent itemset mining
def get_freqitemsets(fname, minsupport, maxlhs, yname=None, header=False, delimiter=' '):
    #minsupport is an integer percentage (e.g. 10 for 10%)
    #maxlhs is the maximum size of the lhs
    #first load the data
    if header:
        data,Y,colnames = load_data(fname, yname=yname, header=header, delimiter=delimiter)
    else:
        data,Y = load_data(fname, yname=yname, header=header, delimiter=delimiter)
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
    if header:
        return X,Y,nruleslen,lhs_len,itemsets_all,colnames,data
    else:
        return X,Y,nruleslen,lhs_len,itemsets_all

def array_to_string(x):
    return list(x).__repr__().replace(',', '').strip('[]')

def titanic(din='../data/titanic', dout='../data/titanic'):
    froot = 'titanic'

    #rule mining parameters
    maxlhs = 2 #maximum cardinality of an itemset
    minsupport = 10 #minimum support (%) of an itemset

    #Do frequent itemset mining from the training data
    fname = os.path.join(din, froot+'_train'+'.tab')
    yname = os.path.join(din, froot+'_train'+'.Y')
    Xtrain,Ytrain,nruleslen,lhs_len,itemsets = get_freqitemsets(fname,minsupport,maxlhs,yname)

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

def driver(din, dout, froot, train_suffix='', y_suffix=None, delimiter=' '):

    #rule mining parameters
    maxlhs = 2 #maximum cardinality of an itemset
    minsupport = 10 #minimum support (%) of an itemset

    #Do frequent itemset mining from the training data
    fname = os.path.join(din, froot + train_suffix)
    if (y_suffix is not None):
        yname = os.path.join(din, froot + y_suffix)
    else:
        yname = None
    (Xtrain, Ytrain, nruleslen, lhs_len, itemsets, colnames, data) = \
        get_freqitemsets(fname, minsupport, maxlhs, yname=yname, header=True, delimiter=delimiter)

    data = np.array(data).T
    features = [list(set(d)) for d in data]
    flat_features = []
    categories_to_features = dict()
    for (fgroup, category) in zip(features, colnames):
        for f in fgroup:
            categories_to_features[f] = category
        flat_features += fgroup
    assert (len(set(flat_features)) == len(flat_features))

    nrules = len(Xtrain)
    ndata = len(Xtrain[0])
    out = []
    for i in range(1, nrules):
        ind = list(Xtrain[i])
        ind.sort()
        row = np.zeros(ndata, int)
        row[ind] = 1
        rule_name = '{%s}' % ','.join(['%s=%s' % (categories_to_features[j], j)
                                       for j in itemsets[i]])
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

def titanic_cols(din='../data/titanic', dout='../data', froot='titanic_cols'):
    driver(din=din, dout=dout, froot=froot, train_suffix='_train.tab', y_suffix='_train.Y')

def telco(din='../data/telco', dout='../data', froot='telco.shuffled'):
    driver(din=din, dout=dout, froot=froot, train_suffix='.txt', delimiter=',')
