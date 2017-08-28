import numpy as np
import pycorels

a = [("{label=0}", np.array([0, 1, 1, 0, 0, 0, 0, 1])), ("{label=1}", np.array([1, 0, 0, 1, 1, 1, 1, 0]))]
b = [("{rule1}", np.array([1,1,1,0,1,1,0,1])), ("{rule2}", np.array([1,0,0,0,1,1,1,0])), ("{rule3}", np.array([1,0,1,0,1,0,1,1]))]

pycorels.run(b, a, verbosity="rule")
