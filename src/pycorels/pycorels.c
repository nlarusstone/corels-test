#include <Python.h>

#include "../queue.hh"
#include "../run.hh"

#define BUFSZ 512s

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
    char* vstring = "silent";
    int log_freq = 0;
    int max_num_nodes = 10000;
    double c = 0.01;
    int ablation = 0;
    int calculate_size = false;

    const char* voptions = "rule|label|samples|progress|log|silent";

    static char* kwlist[] = {"out_file", "label_file", "minor_file", "opt_file", "log_file", "curiosity_policy", "latex_out", "map_type",
                             "verbosity", "log_freq", "max_num_nodes", "c", "ablation", "calculate_size"};

    if(!PyArg_ParseTupleAndKeywords(args, keywds, "ss|sssibisiidibb", kwlist, &out_file, &label_file, &minor_file,
                                    &opt_file, &log_file, &curiosity_policy, &latex_out, &map_type, &vstring,
                                    &log_freq, &max_num_nodes, &c, &ablation, &calculate_size))
    {
        return NULL;
    }

    int verr = 0;
    char* vopt = strtok(vstring, ",");
    while (vopt != NULL) {
        if (!strstr(voptions, vopt)) {
            verr = 1;
            break;
        }
        verbosity.insert(vopt);
        vopt = strtok(NULL, ",");
    }

    int error = 0;
    char* error_txt[BUFSZ];

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
    if (verr) {
        error = 1;
        snprintf(error_txt, BUFSZ, "verbosity options must be one or more of (%s), separated with commas (i.e. -v progress,log)", voptions);
    }
    if (verbosity.count("samples") && !(verbosity.count("rule") || verbosity.count("label"))) {
        error = 1;
        snprintf(error_txt, BUFSZ, "verbosity 'samples' option must be combined with at least one of (rule|label)");
    }
    if (verbosity.size() > 2 && verbosity.count("silent")) {
        error = 1;
        snprintf(error_txt, BUFSZ, "verbosity 'silent' option must be passed without any additional verbosity parameters");
    }

    if (error) {
        PyErr_SetString(PyExc_ValueError, error_txt);
        return NULL;
    }

    if (verbosity.size() == 0) {
        verbosity.insert("progress");
    }

    if (verbosity.count("silent")) {
        verbosity.clear();
    }

    int nrules, nsamples, nlabels, nsamples_chk;
    rule_t *rules, *labels;
    if(rules_init(out_file, &nrules, &nsamples, &rules, 1) != 0) {
        PyErr_SetString(PyExc_ValueError, "could not load out file at path '%s'", out_file);
        return NULL;
    }
    if(rules_init(label_file, &nlabels, &nsamples_chk, &labels, 0) != 0) {
        rules_free(rules, nrules, 1);
        PyErr_SetString(PyExc_ValueError, "could not load label file at path '%s'", label_file);
        return NULL;
    }

    int nmeta, nsamples_check;

    rule_t* meta = NULL;
    if (minor_file && strlen(minor_file)) {
        if(rules_init(minor_file, &nmeta, &nsamples_check, &meta, 0) != 0) {
            rules_free(rules, nrules, 1);
            rules_free(labels, nlabels, 0);
            PyErr_SetString(PyExc_ValueError, "could not load minor file at path '%s'", minor_file);
            return NULL;
        }
    }

    if(nsamples != nsamples_chk) {
        PyErr_SetString(PyExc_ValueError, "rule and label data must contain the same number of samples");
        return NULL;
    }

    if(meta && nsamples != nsamples_check) {
        PyErr_SetString(PyExc_ValueError, "rule and minority data must contain the same number of samples");
        return NULL;
    }

    run_corels(opt_file, log_file, max_num_nodes, c, verbosity, curiosity_policy, map_type,
                    log_freq, ablation, calculate_size, latex_out, nrules, nlabels,
                    nsamples, rules, labels, meta);

    rules_free(rules, nrules, 1);
    rules_free(labels, nlabels, 0);

    if(meta)
        rules_free(meta, nmeta, 0);

    return Py_None;
}

static PyMethodDef pycorelsMethods[] = {
    {"run", pycorels_run, METH_VARARGS | METH_KEYWORDS },
    {NULL, NULL, 0, NULL}
};

PyMODINITFUNC initpycorels(void)
{
    Py_InitModule("pycorels", pycorelsMethods);
}
