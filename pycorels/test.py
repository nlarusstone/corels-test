import numpy as np
import pycorels

#a = [("{label=0}", np.array([0, 1, 1, 0, 0, 0, 0, 1])), ("{label=1}", np.array([1, 0, 0, 1, 1, 1, 1, 0]))]
#b = [("{rule1}", np.array([1,1,1,0,1,1,0,1])), ("{rule2}", np.array([1,0,0,0,1,1,1,0])), ("{rule3}", np.array([1,0,1,0,1,0,1,1]))]

def csplit(rules, indices):

    indices_or_sections = []
    out = []
    numsections = 0

    if not isinstance(indices, list):
        nsamples = len(rules[0][1])
        for i in range(1, indices):
            indices_or_sections.append(int(round(i * nsamples / indices)))

        numsections = indices;
    else:
        indices_or_sections = indices
        numsections = len(indices_or_sections) + 1

    for i in range(numsections):
        out.append([])

    print(indices_or_sections)

    i = 0
    for rule in rules:
        splitlist = np.split(rule[1], indices_or_sections)

        j = 0
        for j in range(len(splitlist)):
            out[j].append((rule[0], splitlist[j]))

    return out

out_file = "../data/adult_R.out"
label_file = "../data/adult_R.label"

verbosity = "progress"

out_list = pycorels.tolist(out_file)
label_list = pycorels.tolist(label_file)

pycorels.tofile(out_list, "compare.out")
pycorels.tofile(label_list, "compare.label")

#pycorels.run(out_file, label_file, verbosity=verbosity)
#pycorels.run(out_list, label_list, verbosity=verbosity)

#out_list = [("1", np.array([0, 1, 1, 0, 1, 2, 3, 4, 5, 1])), ("2", np.array([1, 0, 0, 1, 4, 5, 6, 7, 1, 2]))]

#s10 = csplit(out_list, 2)

#print(out_list)
#print("\n\n")
#print(s10)
