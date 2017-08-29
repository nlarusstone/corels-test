#include <Python.h>

#define NPY_NO_DEPRECATED_API NPY_API_VERSION

#include <numpy/arrayobject.h>

#include "../src/run.hh"

#include "../src/rule.h"

#define BUFSZ  512
#define RULE_INC  100

int CheckString(PyObject** string)
{
    int unicode = 0;
    if(!PyBytes_Check(*string) && !(unicode = PyUnicode_Check(*string)))
        return 1;

    if(unicode)
        *string = PyUnicode_AsASCIIString(*string);

    return 0;
}

/*int load_list(PyObject *list, int *nrules, int *nsamples, rule_t **rules_ret, int add_default_rule)
{
    char *rulestr;
	int rule_cnt, sample_cnt, rsize;
	int i, ones, ret;
	rule_t *rules=NULL;
	size_t len = 0;

	sample_cnt = rsize = 0;

    if(!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "Data must be a python list");
        goto err;
    }

    Py_ssize_t list_len = PyList_Size(list);

    int ntotal_rules = list_len + (add_default_rule != 0 ? 1 : 0);

    PyObject* tuple;
    PyObject* vector;
    PyObject* features;

	rule_cnt = add_default_rule != 0 ? 1 : 0;
	while (rule_cnt < ntotal_rules) {
        if(!(tuple = PyList_GetItem(list, rule_cnt - (add_default_rule != 0 ? 1 : 0))))
            goto err;

        if(!PyTuple_Check(tuple)) {
            PyErr_SetString(PyExc_TypeError, "Array members must be tuples");
            goto err;
        }

		if (rule_cnt >= rsize) {
			rsize += RULE_INC;
            rules = realloc(rules, rsize * sizeof(rule_t));
			if (rules == NULL)
				goto err;
		}

        if(!(features = PyTuple_GetItem(tuple, 0)))
            goto err;

        if(CheckString(&features) != 0) {
            PyErr_SetString(PyExc_TypeError, "The first argument of every tuple must be a string or unicode object");
            goto err;
        }

        rulestr = PyBytes_AsString(features);

		if ((rules[rule_cnt].features = strdup(rulestr)) == NULL)
			goto err;

        if(!(vector = PyTuple_GetItem(tuple, 1)))
            goto err;

        if(!PyArray_Check(vector)) {
            PyErr_SetString(PyExc_TypeError, "The second argument of every tuple must be a numpy array");
            goto err;
        }

        int type = PyArray_TYPE((PyArrayObject*)vector);
        if(PyArray_NDIM((PyArrayObject*)vector) != 1 && (PyTypeNum_ISINTEGER(type) || PyTypeNum_ISBOOL(type))) {
            PyErr_SetString(PyExc_TypeError, "Each rule truthable must be a 1-d array of integers or booleans");
            goto err;
        }

        PyArrayObject* clean = (PyArrayObject*)PyArray_FromAny(vector, PyArray_DescrFromType(NPY_BYTE), 0, 0, NPY_ARRAY_CARRAY | NPY_ARRAY_ENSURECOPY | NPY_ARRAY_FORCECAST, NULL);
        if(clean == NULL) {
            PyErr_SetString(PyExc_Exception, "Could not cast array to byte carray");
            goto err;
        }

        char* data = PyArray_BYTES(clean);
        len = (int)PyArray_SIZE(clean);

        for(int j = 0; j < len; j++)
            data[j] = '0' + !!data[j];

		data[len] = '\0';

		if (ascii_to_vector(data, len, &sample_cnt, &ones,
		    &rules[rule_cnt].truthtable) != 0)
		    	goto err;
		rules[rule_cnt].support = ones;

        printf("%s nsamples: %d\n", rulestr, sample_cnt);

        //printf("%d\n", mpz_sizeinbase(rules[rule_cnt].truthtable, 2));

        Py_DECREF(clean);

		rules[rule_cnt].cardinality = 1;
		for (char *cp = rulestr; *cp != '\0'; cp++)
			if (*cp == ',')
				rules[rule_cnt].cardinality++;
		rule_cnt++;
	}

	if (add_default_rule) {
		rules[0].support = sample_cnt;
		rules[0].features = "default";
		rules[0].cardinality = 0;
		if (make_default(&rules[0].truthtable, sample_cnt) != 0)
		    goto err;
	}

	*nsamples = sample_cnt;
	*nrules = rule_cnt;
	*rules_ret = rules;

	return (0);

err:
	ret = errno;

	if (rules != NULL) {
		for (i = 1; i < rule_cnt; i++) {
			free(rules[i].features);
#ifdef GMP
			mpz_clear(rules[i].truthtable);
#else
			free(rules[i].truthtable);
#endif
		}
		free(rules);
	}
	return (ret);
}*/

int load_list(PyObject* list, int* nrules, int* nsamples, rule_t** rules_ret, int add_default_rule)
{
    rule_t* rules = NULL;

    if(!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "Data must be a python list");
        goto error;
    }

    Py_ssize_t list_len = PyList_Size(list);

    int ntotal_rules = list_len + (add_default_rule ? 1 : 0);

    rules = malloc(sizeof(rule_t) * ntotal_rules);
    if(!rules) {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate rule array");
        goto error;
    }

    int samples_cnt = 0;

    PyObject* tuple;
    PyObject* vector;
    PyObject* features;

    int rule_idx = ntotal_rules - list_len;
    for(Py_ssize_t i = 0; i < list_len; i++) {
        if(!(tuple = PyList_GetItem(list, i)))
            goto error;

        if(!PyTuple_Check(tuple)) {
            PyErr_SetString(PyExc_TypeError, "Array members must be tuples");
            goto error;
        }

        if(!(features = PyTuple_GetItem(tuple, 0)))
            goto error;

        if(CheckString(&features) != 0) {
            PyErr_SetString(PyExc_TypeError, "The first argument of every tuple must be a string or unicode object");
            goto error;
        }

        Py_ssize_t features_len = PyBytes_Size(features);
        rules[rule_idx].features = malloc(features_len + 1);
        strcpy(rules[rule_idx].features, PyBytes_AsString(features));
        //rule[rule_idx].features[features_len] = '\0';

        rules[rule_idx].cardinality = 1;

        if(!(vector = PyTuple_GetItem(tuple, 1)))
            goto error;

        if(!PyArray_Check(vector)) {
            PyErr_SetString(PyExc_TypeError, "The second argument of every tuple must be a numpy array");
            goto error;
        }

        int type = PyArray_TYPE((PyArrayObject*)vector);
        if(PyArray_NDIM((PyArrayObject*)vector) != 1 && (PyTypeNum_ISINTEGER(type) || PyTypeNum_ISBOOL(type))) {
            PyErr_SetString(PyExc_TypeError, "Each rule truthable must be a 1-d array of integers or booleans");
            goto error;
        }

        PyArrayObject* clean = (PyArrayObject*)PyArray_FromAny(vector, PyArray_DescrFromType(NPY_BYTE), 0, 0, NPY_ARRAY_CARRAY | NPY_ARRAY_ENSURECOPY | NPY_ARRAY_FORCECAST, NULL);
        if(clean == NULL) {
            PyErr_SetString(PyExc_Exception, "Could not cast array to byte carray");
            goto error;
        }

        char* data = PyArray_BYTES(clean);
        npy_intp b_len = PyArray_SIZE(clean);

        for(npy_intp j = 0; j < b_len; j++)
            data[j] = '0' + !!data[j];

        data[b_len] = '\0';

        if(ascii_to_vector(data, b_len, &samples_cnt, &rules[rule_idx].support, &rules[rule_idx].truthtable) != 0) {
            PyErr_SetString(PyExc_Exception, "Could not load bit vector");
            goto error;
        }

        Py_DECREF(clean);

        rule_idx++;
    }

    if(add_default_rule) {
        rules[0].support = samples_cnt;
		rules[0].features = "default";
		rules[0].cardinality = 0;
		if (make_default(&rules[0].truthtable, samples_cnt) != 0) {
            PyErr_SetString(PyExc_Exception, "Could not make default rule");
		    goto error;
        }
    }

    *nrules = ntotal_rules;
    *rules_ret = rules;
    *nsamples = samples_cnt;

    return 0;

error:
    if(rules != NULL) {
        for (int i = 1; i < rule_idx; i++) {
            free(rules[i].features);
#ifdef GMP
            mpz_clear(rules[i].truthtable);
#else
            free(rules[i].truthtable);
#endif
        }
        free(rules);
    }
    *rules_ret = NULL;
    *nrules = 0;
    *nsamples = 0;
    return 1;
}

static PyObject* pycorels_run(PyObject* self, PyObject* args, PyObject* keywds)
{
    PyObject* out_data;
    char* out_fname = NULL;

    PyObject* label_data;
    char* label_fname = NULL;

    PyObject* minor_data = NULL;
    char* minor_fname = NULL;

    run_params_t params;
    set_default_params(&params);

    static char* kwlist[] = {"out_data", "label_data", "minor_data", "opt_file", "log_file", "curiosity_policy", "latex_out", "map_type",
                             "verbosity", "log_freq", "max_num_nodes", "c", "ablation", "calculate_size"};

    if(!PyArg_ParseTupleAndKeywords(args, keywds, "OO|Ossibisiidibb", kwlist, &out_data, &label_data, &minor_data,
                                    &params.opt_fname, &params.log_fname, &params.curiosity_policy, &params.latex_out, &params.map_type, &params.vstring,
                                    &params.freq, &params.max_num_nodes, &params.c, &params.ablation, &params.calculate_size))
    {
        return NULL;
    }

    char error_txt[BUFSZ];
    PyObject* error_type = PyExc_ValueError;

    if(CheckString(&out_data)) {
        out_fname = PyBytes_AsString(out_data);
        if(!out_fname || !strlen(out_fname)) {
            snprintf(error_txt, BUFSZ, "out file must be a valid file path");
            goto error;
        }
    }
    else if(PyList_Check(out_data)) {
        if(!PyList_Size(out_data)) {
            snprintf(error_txt, BUFSZ, "out list must be non-empty");
            goto error;
        }
    }
    else {
        snprintf(error_txt, BUFSZ, "out data must be either a python list or a file path");
        error_type = PyExc_TypeError;
        goto error;
    }

    if(CheckString(&label_data)) {
        label_fname = PyBytes_AsString(label_data);
        if(!label_fname || !strlen(label_fname)) {
            snprintf(error_txt, BUFSZ, "label file must be a valid file path");
            goto error;
        }
    }
    else if(PyList_Check(label_data)) {
        if(!PyList_Size(label_data)) {
            snprintf(error_txt, BUFSZ, "label list must be non-empty");
            goto error;
        }
    }
    else {
        snprintf(error_txt, BUFSZ, "label data must be either a python list or a file path");
        error_type = PyExc_TypeError;
        goto error;
    }

    if(minor_data) {
        if(CheckString(&minor_data)) {
            minor_fname = PyBytes_AsString(minor_data);
            if(!minor_fname || !strlen(minor_fname)) {
                snprintf(error_txt, BUFSZ, "minor file must be a valid file path");
                goto error;
            }
        }
        else if(PyList_Check(minor_data)) {
            if(!PyList_Size(minor_data)) {
                snprintf(error_txt, BUFSZ, "minor list must be non-empty");
                goto error;
            }
        }
        else {
            snprintf(error_txt, BUFSZ, "minor data must be either a python list or a file path");
            error_type = PyExc_TypeError;
            goto error;
        }
    }

    if(!params.opt_fname || !strlen(params.opt_fname)) {
        snprintf(error_txt, BUFSZ, "optimal rulelist file must be a valid file path");
        goto error;
    }
    if(!params.log_fname || !strlen(params.log_fname)) {
        snprintf(error_txt, BUFSZ, "log file must be a valid file path");
        goto error;
    }
    if (params.max_num_nodes < 0) {
        snprintf(error_txt, BUFSZ, "maximum number of nodes must be positive");
        goto error;
    }
    if (params.c < 0.0) {
        snprintf(error_txt, BUFSZ, "regularization constant must be postitive");
        goto error;
    }
    if (params.map_type > 2 || params.map_type < 0) {
        snprintf(error_txt, BUFSZ, "symmetry-aware map must be (0|1|2)");
        goto error;
    }
    if (params.curiosity_policy < 0 || params.curiosity_policy > 4) {
        snprintf(error_txt, BUFSZ, "you must specify a curiosity type (0|1|2|3|4)");
        goto error;
    }

    if(out_fname) {
        if(rules_init(out_fname, &params.nrules, &params.nsamples, &params.rules, 1) != 0) {
            snprintf(error_txt, BUFSZ, "could not load out file at path '%s'", out_fname);
            goto error;
        }
    } else {
        if(load_list(out_data, &params.nrules, &params.nsamples, &params.rules, 1) != 0)
            return NULL;
    }

    int nsamples_chk;
    if(label_fname) {
        if(rules_init(label_fname, &params.nlabels, &nsamples_chk, &params.labels, 0) != 0) {
            rules_free(params.rules, params.nrules, 1);
            snprintf(error_txt, BUFSZ, "could not load label file at path '%s'", label_fname);
            goto error;
        }
    } else {
        if(load_list(label_data, &params.nlabels, &nsamples_chk, &params.labels, 0) != 0) {
            rules_free(params.rules, params.nrules, 1);
            return NULL;
        }
    }

    int nmeta, nsamples_check;

    params.meta = NULL;
    if (minor_data) {
        if(minor_fname) {
            if(rules_init(minor_fname, &nmeta, &nsamples_check, &params.meta, 0) != 0) {
                rules_free(params.rules, params.nrules, 1);
                rules_free(params.labels, params.nlabels, 0);
                snprintf(error_txt, BUFSZ, "could not load minority file at path '%s'", minor_fname);
                goto error;
            }
        } else {
            if(load_list(minor_data, &nmeta, &nsamples_check, &params.meta, 0) != 0) {
                rules_free(params.rules, params.nrules, 1);
                rules_free(params.labels, params.nlabels, 0);
                return NULL;
            }
        }
    }

    for(int i = 1; i < params.nrules; i++) {
        printf("params.rules[%d].features = %s\n", i, params.rules[i].features);
    }
    rule_print_all(params.rules + 1, params.nrules - 1, params.nsamples, 1);

    if(params.nsamples != nsamples_chk) {
        rules_free(params.rules, params.nrules, 1);
        rules_free(params.labels, params.nlabels, 0);
        if(params.meta)
            rules_free(params.meta, nmeta, 0);

        snprintf(error_txt, BUFSZ, "the number of samples in the out file (%d) and label file (%d) must match", params.nsamples, nsamples_chk);
        goto error;
    }
    if(params.meta && params.nsamples != nsamples_check) {
        rules_free(params.rules, params.nrules, 1);
        rules_free(params.labels, params.nlabels, 0);
        rules_free(params.meta, nmeta, 0);

        snprintf(error_txt, BUFSZ, "the number of samples in the out file (%d) and minority file (%d) must match", params.nsamples, nsamples_check);
        goto error;
    }

    run_corels(params);

    rules_free(params.rules, params.nrules, 1);
    rules_free(params.labels, params.nlabels, 0);

    if(params.meta)
        rules_free(params.meta, nmeta, 0);

    return Py_None;

error:

    PyErr_SetString(error_type, error_txt);

    return NULL;
}

static PyMethodDef pycorelsMethods[] = {
    {"run", (PyCFunction)pycorels_run, METH_VARARGS | METH_KEYWORDS },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pycorelsModule = {
    PyModuleDef_HEAD_INIT,
    "pycorels",
    "Python binding to CORELS algorithm",
    -1,
    pycorelsMethods
};

PyMODINIT_FUNC PyInit_pycorels(void)
{
    import_array();

    return PyModule_Create(&pycorelsModule);
}
