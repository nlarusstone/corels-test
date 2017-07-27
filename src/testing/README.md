This folder contains code and data files for testing our data structures and algorithm

To compile the tests, simply run 'make tests' from the /src folder (not this folder), and then run './tests' to execute all the tests. If you wish to test only one part of the system, enter './tests [name]' where name is one of the following:

            Name                Description
    -   prefixmap       Test the prefix permutation map
    -   trie            Test the rulelist trie
    -   queue           Test the priority queue

    -   trie_init       Test the initialization of the trie
    -   construct_node  Test the construction of a node by the trie
    -   delete_node     Test the deletion of a node by the trie
    -   node_prefix     Test getting the prefix and predictions from a node
    -   num_eval        Test the trie's behavior with the number of evaluated nodes
    -   num_nodes       Test the trie's decrement_num_nodes function
    -   min_obj         Test the the storing of the minimum objective
    -   prune_up        Test the trie's prune_up function
    -   check_prefix    Test the ability of the trie to check a prefix
    -   delete_subtree  Test the trie's delete_subtree function
    -   optimal_list    Test the trie's storing of the optimal rule list
    -   optimal_pred    Test the trie's storing of the optimal predictions

    -   prefix_empty    Test inserting into an empty prefix permutation map
    -   prefix_higher   Test inserting a prefix with a higher lower bound than
                        previously stored into the prefix permutation map
    -   prefix_lower    Test inserting a prefix with a lower lower bound than
                        previously stored into the prefix permutation map

    -   capture_empty   Test inserting into an empty captured permutation map
    -   capture_higher  Test inserting a prefix with a higher lower bound than
                        previously stored into the captured permutation map
    -   capture_lower   Test inserting a prefix with a lower lower bound than
                        previously stored into the captured permutation map

    -   push            Test pushing to the priority queue
    -   pop             Test popping the priority queue

For example, './tests [prefixmap]' would only run the tests for the prefix permutation map.
