import numpy as np
import tabular as tb


def to_binary(x):
    columns = []
    names = []
    for n in x.dtype.names:
        dlist = list(set(x[n]))
        dlist.sort()
        print n, dlist
        if (len(dlist) == 2):
            if hasattr(dlist[0], 'split'):
                if ('=not-' in dlist[0]):
                    dlist = dlist[1:]
                else:
                    dlist = dlist[:1]
            else:
                dlist = dlist[1:]
        for d in dlist:
            names.append('%s:%s' % (n, str(d)))
            columns.append(np.cast[int](x[n] == d))
    y = tb.tabarray(columns=columns, names=names)
    return y
