import numpy as np
import pylab
import tabular as tb

pylab.ion()
pylab.figure(1, figsize=(8, 3.6))
pylab.clf()
ax = pylab.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=19)

#True Positive, False Negative, False Positive, True Negative
ct = []
reg = np.array([0.01, 0.005, 0.01, 0.005, 0, 0, 0, 0])
loc = np.array([1, 1, 0, 0, 0, 0, 0, 0])
thresh = np.array([0, 0, 0, 0, 4, 3, 2, 1])
cvec = ['m', 'm', 'c', 'c'] + ['w'] * 4
ms = [13, 9, 13, 9] + [12, 10, 8, 6] 
marker = ['s', 's', '^', '^'] + ['o'] * 4
legend = ['CORELS (.01, location)', 'CORELS (.005, location)', 'CORELS (.01)', 'CORELS (.005)'] + [u'Heuristic (\u2265%d)' % i for i in [4, 3, 2, 1]]
fs = 14
nfolds = 10

# python2 eval_model.py cpw -n 100000000 -r 0.01 -c 2 -p 1 -v 10 --minor --parallel
ctables = np.array([[435, 653, 1001, 30490], [439, 649, 990, 30501], [437, 651, 970, 30521], [471, 617, 949, 30542], [438, 650, 1031, 30460], [454, 634, 1026, 30465], [435, 653, 988, 30503], [438, 650, 1014, 30477], [423, 665, 1002, 30489], [457, 631, 946, 30545]])
ct += [ctables.mean(axis=0)]

# python2 eval_model.py cpw -n 100000000 -r 0.005 -c 2 -p 1 -v 10 --minor --parallel
ctables = np.array([[565, 523, 3724, 27767], [541, 547, 3734, 27757], [555, 533, 3753, 27738], [575, 513, 3604, 27887], [549, 539, 3663, 27828], [559, 529, 3669, 27822], [569, 519, 3757, 27734], [545, 543, 3641, 27850], [550, 538, 3706, 27785], [648, 440, 5567, 25924]])
ct += [ctables.mean(axis=0)]

# python2 eval_model.py cpw-noloc -n 100000000 -r 0.01 -c 2 -p 1 -v 10 --minor --parallel
ctables = np.array([[490, 598, 3870, 27621], [508, 580, 3871, 27620], [508, 580, 3828, 27663], [534, 554, 3775, 27716], [505, 583, 3910, 27581], [508, 580, 3850, 27641], [503, 585, 3761, 27730], [503, 585, 3932, 27559], [493, 595, 3885, 27606], [522, 566, 3806, 27685]])
ct += [ctables.mean(axis=0)]

# python2 eval_model.py cpw-noloc -n 100000000 -r 0.005 -c 2 -p 1 -v 10 --minor --parallel
ctables = np.array([[625, 463, 6468, 25023], [602, 486, 6377, 25114], [624, 464, 6538, 24953], [646, 442, 6495, 24996], [629, 459, 6462, 25029], [630, 458, 6555, 24936], [589, 499, 6263, 25228], [620, 468, 6225, 25266], [638, 450, 6559, 24932], [655, 433, 6389, 25102]])
ct += [ctables.mean(axis=0)]

csum = np.zeros((4, 4))
for fold in range(nfolds):
    fname = '../data/CrossValidation/cpw-noloc_%d_test-binary.csv' % fold
    y = tb.tabarray(SVfile=fname)
    z = 3 * y['cs_objcs:stop-reason=suspicious-object'] + y['ac_stsnd:circumstances=sights-and-sounds-of-criminal-activity'] + y['cs_bulge:stop-reason=suspicious-bulge']
    cfold = []
    for t in [4, 3, 2, 1]:
        yes = (z >= t)
        no = np.invert(yes)
        weapon = (y['weapon:1'] == 1)
        nw = np.invert(y['weapon:1'])
        tp = (yes & weapon).sum()
        fn = (no & weapon).sum()
        fp = (yes & nw).sum()
        tn = (no & nw).sum()
        cfold += [[tp, fn, fp, tn]]
    csum += np.array(cfold)
ct += [c for c in (csum / float(nfolds))]
    
ct = [c for c in np.array(ct).T]
(tp, fn, fp, tn) = ct

n = (tp + tn + fp + fn)
acc = (tp + tn) / n
tpr = tp / (tp + fn)
fpr = fp / (fp + tn)
pos = (tp + fp) / n

print 'accuracy:', acc
print 'tpr:', tpr
print 'fpr:', fpr

for i in range(len(tp)):
    pylab.plot(pos[i], tpr[i], marker=marker[i], markersize=ms[i], color=cvec[i], markeredgecolor='k', markeredgewidth=1, linestyle="None")
    print pos[i], tpr[i]

pylab.axis([0, 0.4, 0, 0.65])
pylab.plot([0, 0.4], [0.5, 0.5], 'k:')
pylab.xlabel('Fraction of stops', fontsize=fs)
pylab.ylabel('Fraction recovered', fontsize=fs)
pylab.title('Fraction of weapons recovered', fontsize=fs)
pylab.xticks(np.arange(0, 0.5, 0.1), fontsize=fs)
pylab.yticks(np.arange(0, 0.7, 0.2), fontsize=fs)
pylab.legend(legend, loc='lower right', fontsize=fs-2, frameon=False, numpoints=1, ncol=2)
pylab.savefig('../figs/cpw.pdf')

"""
tail ../logs/*cpw_*100000000*0.005*opt*
{cs_objcs:stop-reason=suspicious-object}~1;{location:transit-authority}~1;{location:housing-authority}~0;{city:MANHATTAN}~1;default~0 --> 7
{cs_objcs:stop-reason=suspicious-object}~1;{location:housing-authority}~0;{location:transit-authority}~1;{city:MANHATTAN}~1;default~0
{cs_objcs:stop-reason=suspicious-object}~1;{location:housing-authority}~0;{city:MANHATTAN}~1;{location:transit-authority}~1;default~0
{cs_objcs:stop-reason=suspicious-object}~1;{location:transit-authority}~1;{city:BRONX}~0;{location:housing-authority}~0;{cs_furtv:stop-reason=furtive-movements}~0;default~1

tail ../logs/*cpw_*100000000*0.01*opt*
{cs_objcs:stop-reason=suspicious-object}~1;{location:transit-authority}~1;default~0 --> 8
{location:transit-authority}~1;{cs_objcs:stop-reason=suspicious-object}~1;default~0 --> 2

tail ../logs/*cpw-noloc*100000000*0.01*opt*
{cs_objcs:stop-reason=suspicious-object}~1;{inout:outside}~0;default~1 --> 7
{cs_objcs:stop-reason=suspicious-object}~1;{inout:inside}~1;default~0 --> 3

tail ../logs/*cpw-noloc_*100000000*0.005*opt*
{cs_objcs:stop-reason=suspicious-object}~1;{cs_lkout:stop-reason=acting-as-lookout}~0;{cs_furtv:stop-reason=furtive-movements}~0;{cs_descr:stop-reason=fits-description}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_descr:stop-reason=fits-description}~0;{cs_lkout:stop-reason=acting-as-lookout}~0;{cs_furtv:stop-reason=furtive-movements}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_furtv:stop-reason=furtive-movements}~0;{cs_lkout:stop-reason=acting-as-lookout}~0;{cs_descr:stop-reason=fits-description}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_lkout:stop-reason=acting-as-lookout}~0;{cs_descr:stop-reason=fits-description}~0;{cs_furtv:stop-reason=furtive-movements}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_furtv:stop-reason=furtive-movements}~0;{cs_lkout:stop-reason=acting-as-lookout}~0;{cs_descr:stop-reason=fits-description}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_furtv:stop-reason=furtive-movements}~0;{cs_descr:stop-reason=fits-description}~0;{cs_lkout:stop-reason=acting-as-lookout}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_lkout:stop-reason=acting-as-lookout}~0;{cs_descr:stop-reason=fits-description}~0;{cs_furtv:stop-reason=furtive-movements}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_descr:stop-reason=fits-description}~0;{cs_casng:stop-reason=casing}~0;{cs_furtv:stop-reason=furtive-movements}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_casng:stop-reason=casing}~0;{cs_descr:stop-reason=fits-description}~0;{cs_furtv:stop-reason=furtive-movements}~0;default~1
{cs_objcs:stop-reason=suspicious-object}~1;{cs_casng:stop-reason=casing}~0;{cs_furtv:stop-reason=furtive-movements}~0;{cs_descr:stop-reason=fits-description}~0;default~1
"""
