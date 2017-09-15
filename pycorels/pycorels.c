#include <Python.h>
#include <string.h>

#define NPY_NO_DEPRECATED_API NPY_API_VERSION

#include <numpy/arrayobject.h>

#include "../src/run.hh"

#include "../src/rule.h"

#include "utils.h"

static PyObject *pycorels_fastmine(PyObject *self, PyObject *args, PyObject *keywds)
{
    const char *base_out_path;
    int max_cardinality;
    double min_support = 0.1;
    GATE *gates = NULL;
    int num_gates;

    int no_repeat = 1;
    int log_freq = 100000;

    PyObject *gates_obj;

    static char* kwlist[] = {"out_file", "max_cardinality", "min_support", "gates", "no_repeat", "log_freq"};

    if(!PyArg_ParseTupleAndKeywords(args, keywds, "sidO|ii", kwlist, &base_out_path, &max_cardinality, &min_support, &gates_obj, &no_repeat, &log_freq)) {
        return NULL;
    }

    if(!PyLong_Check(gates_obj)) {
        PyErr_SetString(PyExc_TypeError, "Gates must be a list");
        return NULL;
    }

    long gates_code = PyLong_AsLong(gates_obj);
    switch(gates_code)
    {
        case 0:
            gates = malloc(sizeof(GATE));
            gates[0] = G_AND;
            num_gates = 1;
            break;
        case 1:
            gates = malloc(sizeof(GATE));
            gates[0] = G_OR;
            num_gates = 1;
            break;
        case 2:
            gates = malloc(2 * sizeof(GATE));
            gates[0] = G_AND;
            gates[1] = G_OR;
            num_gates = 2;
            break;
        default:
            num_gates = 0;
            break;
    };

    int nsamples;
    rule_t **rules = malloc(sizeof(rule_t*) * max_cardinality);
    int *nrules = malloc(sizeof(int) * max_cardinality);

    contains_t **contains = malloc(sizeof(contains_t*) * max_cardinality);

    if(rules_init(base_out_path, &nrules[0], &nsamples, &rules[0], 0) != 0) {
        PyErr_SetString(PyExc_IOError, "Could not load base out file\n");
        free(rules);
        free(nrules);
        return NULL;
    }

    printf("samples: %d\n", nsamples);

    contains[0] = malloc(sizeof(contains_t) * nrules[0]);

    if(no_repeat) {
        for(int i = 0; i < nrules[0]; i++) {
            contains[0][i].data = malloc(sizeof(int));
            *(contains[0][i].data) = i;
            contains[0][i].len = 1;
        }
    }

    int total_rule_idx = 0;
    // card is actually one less than the cardinality it represents
    for(int card = 1; card < max_cardinality; card++) {
        int rule_idx = 0;

        rules[card] = NULL;

        if(no_repeat)
            contains[card] = NULL;

        for(int rule1_idx = 0; rule1_idx < nrules[card-1]; rule1_idx++) {
            for(int rule2_idx = (card == 1 ? rule1_idx+1 : 0); rule2_idx < nrules[0]; rule2_idx++) {
                if(no_repeat) {
                    int isin = 0;
                    for(int j = 0; j < contains[card-1][rule1_idx].len; j++) {
                        if(contains[card-1][rule1_idx].data[j] == rule2_idx) {
                            isin = 1;
                            break;
                        }
                    }

                    if(isin)
                        continue;
                }

                for(int gate = 0; gate < num_gates; gate++) {
                    rule_t temp;
                    contains_t tcont;
                    contains_t *src1_contains = NULL, *src2_contains = NULL;

                    if(no_repeat) {
                        src1_contains = &contains[card-1][rule1_idx];
                        src2_contains = &contains[0][rule2_idx];
                    }

                    if(generate_rule(&temp, rules[card-1][rule1_idx], rules[0][rule2_idx], gates[gate], nsamples, min_support, no_repeat, &tcont, src1_contains, src2_contains) == 0) {
                        if(rules[card] == NULL)
                            rules[card] = malloc(sizeof(rule_t) * (rule_idx + 1));
                        else
                            rules[card] = realloc(rules[card], sizeof(rule_t) * (rule_idx + 1));

                        if(no_repeat) {
                            if(contains[card] == NULL)
                                contains[card] = malloc(sizeof(contains_t) * (rule_idx + 1));
                            else
                                contains[card] = realloc(contains[card], sizeof(contains_t) * (rule_idx + 1));
                        }

                        memcpy(&rules[card][rule_idx], &temp, sizeof(rule_t));
                        if(no_repeat)
                            memcpy(&contains[card][rule_idx], &tcont, sizeof(contains_t));

                        total_rule_idx++;
                        if(total_rule_idx % log_freq == 0)
                            printf("Generated %d rules\n", total_rule_idx);

                        rule_idx++;
                    }
                }
            }
        }

        nrules[card] = rule_idx;
        //printf("%d\n", rule_idx);
    }

    total_rule_idx += nrules[0];

    printf("total: %d\n", total_rule_idx);

    PyObject *list = PyList_New(total_rule_idx);

    int start = 0;
    for(int i = 0; i < max_cardinality; i++) {
        if(!fill_list(list, rules[i], start, nrules[i], nsamples)) {
            Py_XDECREF(list);
            list = NULL;
            break;
        }
        start += nrules[i];
    }

    for(int i = 0; i < max_cardinality; i++) {
        for(int j = 0; j < nrules[i]; j++) {
            mpz_clear(rules[i][j].truthtable);
            if(no_repeat)
                free(contains[i][j].data);
            free(rules[i][j].features);
        }
        free(rules[i]);
        if(no_repeat)
            free(contains[i]);
    }

    if(gates)
        free(gates);

    free(contains);
    free(rules);
    free(nrules);

    return list;
}

static PyObject *pycorels_tofile(PyObject *self, PyObject *args)
{
    PyObject *list;
    const char *fname;

    if(!PyArg_ParseTuple(args, "Os", &list, &fname))
        return NULL;

    if(!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a list");
        return NULL;
    }

    PyObject *tuple, *vector;
    char *features;

    npy_intp list_len = PyList_Size(list);

    FILE *fp;
    if(!(fp = fopen(fname, "w")))
        return NULL;

    for(Py_ssize_t i = 0; i < list_len; i++) {
        if(!(tuple = PyList_GetItem(list, i)))
            goto error;

        if(!PyTuple_Check(tuple)) {
            PyErr_SetString(PyExc_TypeError, "Array members must be tuples");
            goto error;
        }

        if(!PyArg_ParseTuple(tuple, "sO", &features, &vector))
            goto error;

        fprintf(fp, "%s ", features);

        int type = PyArray_TYPE((PyArrayObject*)vector);
        if(PyArray_NDIM((PyArrayObject*)vector) != 1 && (PyTypeNum_ISINTEGER(type) || PyTypeNum_ISBOOL(type))) {
            PyErr_SetString(PyExc_TypeError, "Each rule truthable must be a 1-d array of integers or booleans");
            goto error;
        }

        PyArrayObject *clean = (PyArrayObject*)PyArray_FromAny(vector, PyArray_DescrFromType(NPY_BYTE), 0, 0, NPY_ARRAY_CARRAY | NPY_ARRAY_ENSURECOPY | NPY_ARRAY_FORCECAST, NULL);
        if(clean == NULL) {
            PyErr_SetString(PyExc_Exception, "Could not cast array to byte carray");
            goto error;
        }

        char *data = PyArray_BYTES(clean);
        npy_intp b_len = PyArray_SIZE(clean);

        for(npy_intp j = 0; j < b_len-1; j++) {
            fprintf(fp, "%d ", !!data[j]);
        }

        fprintf(fp, "%d\n", !!data[b_len-1]);

        Py_DECREF(clean);
    }

    fclose(fp);

    Py_INCREF(Py_None);
    return Py_None;

error:
    fclose(fp);
    return NULL;
}

static PyObject *pycorels_tolist(PyObject *self, PyObject *args)
{
    const char *fname;

    if(!PyArg_ParseTuple(args, "s", &fname))
        return NULL;

    rule_t *rules;
    int nrules, nsamples;

    if(rules_init(fname, &nrules, &nsamples, &rules, 0) != 0) {
        PyErr_SetString(PyExc_ValueError, "Could not load rule file");
        return NULL;
    }

    PyObject *list = PyList_New(nrules);

    PyObject *res = fill_list(list, rules, 0, nrules, nsamples);
    if(!res) {
        Py_XDECREF(list);
        list = NULL;
    }

    rules_free(rules, nrules, 0);

    return list;
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

    if(PyBytes_Check(out_data)) {
        if(!(out_fname = strdup(PyBytes_AsString(out_data))))
            return NULL;
    }
    else if(PyUnicode_Check(out_data)) {
        PyObject* bytes = PyUnicode_AsUTF8String(out_data);
        if(!bytes)
            return NULL;

        else if(!(out_fname = strdup(PyBytes_AsString(bytes))))
            return NULL;

        Py_DECREF(bytes);
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

    if(PyBytes_Check(label_data)) {
        if(!(label_fname = strdup(PyBytes_AsString(label_data))))
            return NULL;
    }
    else if(PyUnicode_Check(label_data)) {
        PyObject* bytes = PyUnicode_AsUTF8String(label_data);
        if(!bytes)
            return NULL;

        else if(!(label_fname = strdup(PyBytes_AsString(bytes))))
            return NULL;

        Py_DECREF(bytes);
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
        if(PyBytes_Check(minor_data)) {
            if(!(minor_fname = strdup(PyBytes_AsString(minor_data))))
                return NULL;
        }
        else if(PyUnicode_Check(minor_data)) {
            PyObject* bytes = PyUnicode_AsUTF8String(minor_data);
            if(!bytes)
                return NULL;

            else if(!(minor_fname = strdup(PyBytes_AsString(bytes))))
                return NULL;

            Py_DECREF(bytes);
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

    //printf("out_fname: %s\n", out_fname);

    if(out_fname) {
        if(rules_init(out_fname, &params.nrules, &params.nsamples, &params.rules, 1) != 0) {
            snprintf(error_txt, BUFSZ, "could not load out file at path '%s'", out_fname);
            goto error;
        }

        free(out_fname);
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

        free(label_fname);
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

            free(minor_fname);
        } else {
            if(load_list(minor_data, &nmeta, &nsamples_check, &params.meta, 0) != 0) {
                rules_free(params.rules, params.nrules, 1);
                rules_free(params.labels, params.nlabels, 0);
                return NULL;
            }
        }
    }

    /*if(params.nsamples != nsamples_chk) {
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
    }*/

    if(params.nlabels != 2) {
        rules_free(params.rules, params.nrules, 1);
        rules_free(params.labels, params.nlabels, 0);
        rules_free(params.meta, nmeta, 0);

        snprintf(error_txt, BUFSZ, "the number of labels in the label file must be 2, not %d", params.nlabels);
        goto error;
    }

    double accuracy = run_corels(params);

    rules_free(params.rules, params.nrules, 1);
    rules_free(params.labels, params.nlabels, 0);

    if(params.meta)
        rules_free(params.meta, nmeta, 0);

    return Py_BuildValue("d", accuracy);

error:

    PyErr_SetString(error_type, error_txt);

    return NULL;
}

static PyMethodDef pycorelsMethods[] = {
    {"run", (PyCFunction)pycorels_run, METH_VARARGS | METH_KEYWORDS },
    {"tolist", (PyCFunction)pycorels_tolist, METH_VARARGS },
    {"tofile", (PyCFunction)pycorels_tofile, METH_VARARGS },
    {"fastmine", (PyCFunction)pycorels_fastmine, METH_VARARGS | METH_KEYWORDS },
    {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION > 2

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

#else

PyMODINIT_FUNC initpycorels(void)
{
    import_array();

    Py_InitModule("pycorels", pycorelsMethods);
}

#endif
