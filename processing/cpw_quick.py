"""
Quick look at CPW

"""
import tabular as tb

y = tb.tabarray(SVfile='../data/frisk/frisk.csv')

idx = np.array([n for (n, i) in enumerate(x['crimsusp']) if ('cpw' in i.lower()) or ('weapon' in i.lower()) or ('gun' in i.lower())])

print 'crime suspected contains "CPW", "weapon", or "gun"', len(idx)

z = y[idx]

predict_weapon = (z['location']=='transit-authority') | (z['cs_objcs']=='stop-reason=suspicious-object') | (z['cs_bulge']=='stop-reason=suspicious-bulge')

not_weapon = np.invert(z['weapon'])
not_predict = np.invert(predict_weapon)
tp = (predict_weapon & z['weapon']).sum()
fp = (predict_weapon & not_weapon).sum()
fn = (not_predict & z['weapon']).sum()
tn = (not_predict & not_weapon).sum()

"""
n = len(z)
n = 5420
tp = 121.
fp = 706.
fn = 105.
tn = 4488.
tpr = tp / (tp + fn)    # 0.54
fpr = fp / (fp + tn)    # 0.14
"""
