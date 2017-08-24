#include <Python.h>

#include "../run.hh"

#define BUFSZ 512

static PyObject* pycorels_run(PyObject* self, PyObject* args, PyObject* keywds)
{
    // Required arguments
    const char* out_file;
    const char* label_file;

    // Optional arguments
    char* minor_file = NULL;
    char* opt_file = "./corels_opt.txt";
    char* log_file = "./corels_log.txt";
    int curiosity_policy = 0;
    int latex_out = 0;
    int map_type = 0;
    char* vstring = "progress";
    int log_freq = 0;
    int max_num_nodes = 10000;
    double c = 0.01;
    int ablation = 0;
    int calculate_size = 0;

    static char* kwlist[] = {"out_file", "label_file", "minor_file", "opt_file", "log_file", "curiosity_policy", "latex_out", "map_type",
                             "verbosity", "log_freq", "max_num_nodes", "c", "ablation", "calculate_size"};

    if(!PyArg_ParseTupleAndKeywords(args, keywds, "ss|sssibisiidibb", kwlist, &out_file, &label_file, &minor_file,
                                    &opt_file, &log_file, &curiosity_policy, &latex_out, &map_type, &vstring,
                                    &log_freq, &max_num_nodes, &c, &ablation, &calculate_size))
    {
        return NULL;
    }

    int error = 0;
    char error_txt[BUFSZ];

    if(!out_file || !strlen(out_file)) {
        error = 1;
        snprintf(error_txt, BUFSZ, "out file must be a valid file path");
    }
    if(!label_file || !strlen(label_file)) {
        error = 1;
        snprintf(error_txt, BUFSZ, "label file must be a valid file path");
    }
    if(!opt_file || !strlen(opt_file)) {
        error = 1;
        snprintf(error_txt, BUFSZ, "optimal rulelist file must be a valid file path");
    }
    if(!log_file || !strlen(log_file)) {
        error = 1;
        snprintf(error_txt, BUFSZ, "log file must be a valid file path");
    }
    if (max_num_nodes < 0) {
        error = 1;
        snprintf(error_txt, BUFSZ, "maximum number of nodes must be positive");
    }
    if (c < 0.0) {
        error = 1;
        snprintf(error_txt, BUFSZ, "regularization constant must be postitive");
    }
    if (map_type > 2 || map_type < 0) {
        error = 1;
        snprintf(error_txt, BUFSZ, "symmetry-aware map must be (0|1|2)");
    }
    if (curiosity_policy < 0 || curiosity_policy > 4) {
        error = 1;
        snprintf(error_txt, BUFSZ, "you must specify a curiosity type (0|1|2|3|4)");
    }

    if (error) {
        PyErr_SetString(PyExc_ValueError, error_txt);
        return NULL;
    }

    int nrules, nsamples, nlabels, nsamples_chk;
    rule_t *rules, *labels;
    if(rules_init(out_file, &nrules, &nsamples, &rules, 1) != 0) {
        PyErr_SetString(PyExc_ValueError, "could not load out file");
        return NULL;
    }
    printf("loaded out file\n");
    if(rules_init(label_file, &nlabels, &nsamples_chk, &labels, 0) != 0) {
        rules_free(rules, nrules, 1);
        PyErr_SetString(PyExc_ValueError, "could not load label file");
        return NULL;
    }
    printf("loaded label file\n");

    int nmeta, nsamples_check;

    rule_t* meta = NULL;
    if (minor_file && strlen(minor_file)) {
        if(rules_init(minor_file, &nmeta, &nsamples_check, &meta, 0) != 0) {
            rules_free(rules, nrules, 1);
            rules_free(labels, nlabels, 0);
            PyErr_SetString(PyExc_ValueError, "could not load minority file");
            return NULL;
        }
        printf("loaded minor file");
    }

    if(nsamples != nsamples_chk) {
        rules_free(rules, nrules, 1);
        rules_free(labels, nlabels, 0);
        if(meta)
            rules_free(meta, nmeta, 0);

        PyErr_SetString(PyExc_ValueError, "the number of samples in the out and label files must match");
        return NULL;
    }
    printf("checked nsamples_chk\n");
    printf("%d %d\n")
    if(meta && nsamples != nsamples_check) {
        printf("Problem with nsamples_check");
        rules_free(rules, nrules, 1);
        rules_free(labels, nlabels, 0);
        if(meta)
            rules_free(meta, nmeta, 0);

        PyErr_SetString(PyExc_ValueError, "the number of samples in the out and minor files must match");
        return NULL;
    }
    printf("checked nsamples_check");

    run_corels(opt_file, log_file, max_num_nodes, c, vstring, curiosity_policy, map_type,
                log_freq, ablation, calculate_size, latex_out, nrules, nlabels, nsamples, rules, labels, meta);

    rules_free(rules, nrules, 1);
    rules_free(labels, nlabels, 0);

    if(meta) {
        rules_free(meta, nmeta, 0);
    }

    return Py_None;
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
