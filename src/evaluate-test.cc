#include "queue.hh"
#include "evaluate.hh"

NullLogger * logger;

int main(int argc, char ** argv)
{
    logger = new NullLogger();

    double obj = evaluate("/home/vassy/code/bbcache/logs/for-votes_R.out-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=100000-c=0.0150000-v=0-f=1000-opt.txt",
                                "../data/votes_R.out", "../data/votes_R.label", 0.015, 5);

    delete logger;

    return (obj == -1.0 ? 1 : 0);
}
