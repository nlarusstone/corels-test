#include "evaluate.hh"

NullLogger * logger;

int main(int argc, char ** argv)
{
    logger = new NullLogger();

    int r = run_random_tests(10, 20, 100, 0.15, 4, 2, lb_cmp, true,
                             100000, 0.0000001, time(NULL), 5);

    delete logger;

    return r;
}
