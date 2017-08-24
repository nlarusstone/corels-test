#include <Python.h>

#include "../src/run.hh"
#include "../src/params.h"

#define BUFSZ 512

static PyObject* pycorels_run(PyObject* self, PyObject* args, PyObject* keywds)
{
    const char* out_fname;
    const char* label_fname;

    char* minor_fname = NULL;

    run_params_t params;
    set_default_params(&params);

    static char* kwlist[] = {"out_file", "label_file", "minor_file", "opt_file", "log_file", "curiosity_policy", "latex_out", "map_type",
                             "verbosity", "log_freq", "max_num_nodes", "c", "ablation", "calculate_size"};

    if(!PyArg_ParseTupleAndKeywords(args, keywds, "ss|sssibisiidibb", kwlist, &out_fname, &label_fname, &minor_fname,
                                    &params.opt_fname, &params.log_fname, &params.curiosity_policy, &params.latex_out, &params.map_type, &params.vstring,
                                    &params.freq, &params.max_num_nodes, &params.c, &params.ablation, &params.calculate_size))
    {
        return NULL;
    }

    char error_txt[BUFSZ];

    if(!out_fname || !strlen(out_fname)) {
        snprintf(error_txt, BUFSZ, "out file must be a valid file path");
        goto error;
    }
    if(!label_fname || !strlen(label_fname)) {
        snprintf(error_txt, BUFSZ, "label file must be a valid file path");
        goto error;
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

    int nsamples_chk;
    if(rules_init(out_fname, &params.nrules, &params.nsamples, &params.rules, 1) != 0) {
        snprintf(error_txt, BUFSZ, "could not load out file at path '%s'", out_fname);
        goto error;
    }
    if(rules_init(label_fname, &params.nlabels, &nsamples_chk, &params.labels, 0) != 0) {
        rules_free(params.rules, params.nrules, 1);
        snprintf(error_txt, BUFSZ, "could not load label file at path '%s'", label_fname);
        goto error;
    }

    int nmeta, nsamples_check;

    if (minor_fname && strlen(minor_fname)) {
        if(rules_init(minor_fname, &nmeta, &nsamples_check, &params.meta, 0) != 0) {
            rules_free(params.rules, params.nrules, 1);
            rules_free(params.labels, params.nlabels, 0);
            snprintf(error_txt, BUFSZ, "could not load minority file at path '%s'", minor_fname);
            goto error;
        }
    }

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

    PyErr_SetString(PyExc_ValueError, error_txt);

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
    return PyModule_Create(&pycorelsModule);
}
