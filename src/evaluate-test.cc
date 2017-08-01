#include "queue.hh"
#include "evaluate.hh"

NullLogger * logger;

int main(int argc, char ** argv)
{
    logger = new NullLogger();

    double obj = evaluate("../logs/for-adult_R.out-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=10000000-c=0.0150000-v=0-f=1000-opt.txt",
                          "../data/adult_R.out", "../data/adult_R.label", 0.015, 5);

    delete logger;

    return (obj == -1.0 ? 1 : 0);
}
