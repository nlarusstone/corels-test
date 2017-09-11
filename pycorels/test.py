import numpy as np
import pycorels

#a = [("{label=0}", np.array([0, 1, 1, 0, 0, 0, 0, 1])), ("{label=1}", np.array([1, 0, 0, 1, 1, 1, 1, 0]))]
#b = [("{rule1}", np.array([1,1,1,0,1,1,0,1])), ("{rule2}", np.array([1,0,0,0,1,1,1,0])), ("{rule3}", np.array([1,0,1,0,1,0,1,1]))]

out_file = "../data/adult_R.out"
label_file = "../data/adult_R.label"

verbosity = "progress"

out_list = pycorels.tolist(out_file)
label_list = pycorels.tolist(label_file)

pycorels.run(out_file, label_file, verbosity=verbosity)
pycorels.run(out_list, label_list, verbosity=verbosity)
