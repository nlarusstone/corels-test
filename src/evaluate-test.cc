#include "queue.hh"
#include "evaluate.hh"

NullLogger * logger;

int main(int argc, char ** argv)
{
    const char * model_file = "../logs/for-evaluate.out-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=100000-c=0.0150000-v=0-f=1000-opt.txt";
    const char * out_file = "../data/evaluate-data/evaluate.out";
    const char * label_file = "../data/evaluate-data/evaluate.label";
    const char * minor_file = NULL; //"../data/evaluate-data/evaluate.minor";
    double c = 0.015;
    double v = 5;

    logger = new NullLogger();


    model_t model;
    if(model_init(&model, model_file, out_file, label_file, minor_file, c, v) != 0) {
        delete logger;
        return 1;
    }

    // Find model's objective
    double m_obj = evaluate(model, v);

    // Run brute force
    /*double obj = obj_brute(model, v);

    if(m_obj == -1.0 || obj == -1.0) {
        if(v > 0)
            printf("[main] Error with objective calculations! Exiting\n");

        delete logger;
        model_free(model);
        return 1;
    }

    double d = m_obj - obj;
    double e = 0.0000001;
    int match = 0;

    if(d < e && d > -e) {
        if(v > 1)
            printf("[main] Minimum objectives match!\n");

        match = 1;
    }
    else if(v > 1) {
        printf("[main] ERROR: Mismatch of minimum objectives:\n" \
               "[main]     model obj: %.10f    brute-force obj: %.10f\n",
               m_obj, obj);
    }*/

    model_free(model);

    delete logger;

    return 0;
}
