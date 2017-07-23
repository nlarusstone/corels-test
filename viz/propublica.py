"""
Quick stats on ProPublica variants and other analysis

"""

"""
$ tail ../logs/for-propublica_*_train.out-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000000-*opt*
{priors:>3}~1;{sex:Male,age:<25}~1;default~0
{sex:Male,age:<25}~1;{priors:>3}~1;default~0
{age:<25,priors:2-3}~1;{age:<25,juvenile-crimes:>0}~1;{priors:>3}~1;default~0
{priors:>3}~1;{sex:Male,age:<25}~1;default~0
{priors:>3}~1;{age:<25,priors:2-3}~1;{age:<25,juvenile-crimes:>0}~1;default~0
{priors:>3}~1;{sex:Male,age:<25}~1;default~0
{sex:Male,age:<25}~1;{priors:>3}~1;default~0
{juvenile-crimes:=0,priors:=0}~0;{sex:Male,age:<25}~1;{priors:>3}~1;default~0
{age:<25,priors:2-3}~1;{priors:>3}~1;{age:<25,juvenile-crimes:>0}~1;default~0
{priors:>3}~1;{sex:Male,age:<25}~1;default~0

"""
print 'coarse age categories + race:  mine 197-198 rules (mean = 197.2)'

c_test = np.array([0.6865464632454924, 0.6601941747572816, 0.665742024965326, 0.6643550624133149, 0.6338418862690708, 0.6574202496532594, 0.636615811373093, 0.6740638002773925, 0.6449375866851595, 0.665742024965326]
)

# Test accuracies mean, std 0.65894590846 0.0156235036776
print 'mean, std', c_test.mean(), c_test.std()

