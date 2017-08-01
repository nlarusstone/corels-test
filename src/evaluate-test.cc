#include "queue.hh"
#include "evaluate.hh"

NullLogger * logger;

int main(int argc, char ** argv)
{
    logger = new NullLogger();

    delete logger;

    return 0;
}
