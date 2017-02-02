# compas, prioritize via lower bound, permutation map, identical points bound

    python eval_model.py compas -k 10 --minor -c 2 -p 1 -r 0.005 -n 3000000 3>&1 | tee ../logs/log-compas-lower_bound

# compas, bfs, permutation map, identical points bound

    python eval_model.py compas --minor -k 1 -c 2 -p 1 -r 0.005 -n 3000000 3>&1 | tee ../logs/log-compas-bfs

# compas, curiosity, permutation map, identical points bound

    python eval_model.py compas --minor -k 1 -c 2 -p 1 -r 0.005 -n 3000000 3>&1 | tee ../logs/log-compas-curiosity

# compas, prioritize via lower bound, no permutation map, identical points bound

    python eval_model.py compas --minor -k 1 -c 2 -p 1 -r 0.005 -n 3000000 3>&1 | tee ../logs/log-compas-no_pmap

# compas, prioritize via lower bound, permutation map, no identical points bound

    python eval_model.py compas --minor -k 11 -c 2 -p 1 -r 0.005 -n 3000000 3>&1 | tee ../logs/log-compas-no_id

