import numpy as np

nrules = 377

k = 20

cache_size = np.array(cache.metrics.cache_size[:k])
inserts = np.array(cache.metrics.inserts[:k])
inferior = np.array(cache.metrics.inferior[:k])

commutes = np.array(cache.metrics.commutes[:k])
dominates = np.array(cache.metrics.dominates[:k])
rejects = np.array(cache.metrics.rejects[:k])

insufficient_captured = np.array(cache.metrics.captured_zero[:k])
insufficient_correct = np.array(cache.metrics.insufficient[:k])
dead_prefix = np.array(cache.metrics.dead_prefix[:k])

garbage_collect = np.array(cache.metrics.garbage_collect[:k])
prune_up = np.array(cache.metrics.prune_up[:k])

x = (cache_size == inserts - inferior - garbage_collect - prune_up).all()
print 'cache size = (inserts - inferior - garbage collect - prune up):', x

not_evaluated = dominates + commutes + rejects
not_inserted = insufficient_captured + insufficient_correct + dead_prefix

check = inserts + not_evaluated + not_inserted
state_space = np.array([np.prod(np.arange(377, 377 - i, -1)) for i in range(k)])

print 'not evaluated = (dominates + commutes + rejects)'
print 'not inserted = (insufficient captured + insufficient correct + dead prefix)'

j = check.nonzero()[0][-1]
y = (state_space[:j] == check[:j]).all()
print 'state space size = (inserts + not evaluated + not inserted):', y, 'for length <', j

evaluated = inserts + not_inserted