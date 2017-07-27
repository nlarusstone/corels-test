/***  MAIN FILE WITH THE ACTUAL TESTS ***/

#include "catch.hpp"

#include "fixtures.hh"

TEST_CASE_METHOD(TrieFixture, "Trie/Test trie initialization", "[trie][trie_init]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    CHECK(tree->num_nodes() == 1);
    CHECK(tree->num_evaluated() == 0);
    CHECK(tree->c() == c);
    CHECK(tree->nsamples() == nsamples);
    CHECK(tree->nrules() == nrules);
    CHECK(tree->ablation() == ablation);
    CHECK(tree->has_minority() == (bool)minority);
    CHECK(tree->calculate_size() == calculate_size);

    // Test that the rules are correctly stored by the tree
    for(int i = 0; i < nrules; i++) {
        CAPTURE(i);
        CHECK(tree->rule(i).support == rules[i].support);
        CHECK(tree->rule(i).cardinality == rules[i].cardinality);
        CHECK(std::string(tree->rule(i).features) == std::string(rules[i].features));
        CHECK(std::string(tree->rule_features(i)) == std::string(rules[i].features));

#ifdef GMP
        CHECK(mpz_cmp(tree->rule(i).truthtable, rules[i].truthtable) == 0);
#else
        for(int j = 0; j < NENTRIES; j++) {
            CAPTURE(j);
            CHECK(tree->rule(i).truthtable[j] == rules[i].truthtable[j]);
        }
#endif
    }

    // Check that the labels are correctly stored by the tree
    for(int i = 0; i < nlabels; i++) {
        CAPTURE(i);
        CHECK(tree->label(i).support == labels[i].support);
        CHECK(tree->label(i).cardinality == labels[i].cardinality);
        CHECK(std::string(tree->label(i).features) == std::string(labels[i].features));

#ifdef GMP
        CHECK(mpz_cmp(tree->label(i).truthtable, labels[i].truthtable) == 0);
#else
        for(int j = 0; j < NENTRIES; j++) {
            CAPTURE(j);
            CHECK(tree->label(i).truthtable[j] == labels[i].truthtable[j]);
        }
#endif
    }

    // Check that the minority info is correctly stored by the tree
    if(minority != NULL) {
        for(int i = 0; i < nminority; i++) {
            CAPTURE(i);
            CHECK(tree->minority(i).support == minority[i].support);
            CHECK(tree->minority(i).cardinality == minority[i].cardinality);
            CHECK(std::string(tree->minority(i).features) == std::string(minority[i].features));

#ifdef GMP
            CHECK(mpz_cmp(tree->minority(i).truthtable, minority[i].truthtable) == 0);
#else
            for(int j = 0; j < NENTRIES; j++) {
                CAPTURE(j);
                CHECK(tree->minority(i).truthtable[j] == minority[i].truthtable[j]);
            }
#endif
        }
    }
}

TEST_CASE_METHOD(TrieFixture, "Trie/Construct and insert node", "[trie][construct_node]") {

    Node * parent = root;

    REQUIRE(tree != NULL);
    REQUIRE(parent != NULL);

    unsigned short rule_id = 1;
    bool prediction = true;
    bool default_prediction = true;
    double lower_bound = 0.1;
    double objective = 0.12;
    int num_not_captured = 5;
    int len_prefix = 0;
    double equivalent_minority = 0.1;

    Node * n = tree->construct_node(rule_id, nrules, prediction, default_prediction,
                                    lower_bound, objective, parent,
                                    num_not_captured, nsamples, len_prefix,
                                    c, equivalent_minority);

    // Was node inserted?
    REQUIRE(n != NULL);

    CHECK(n->id() == rule_id);
    CHECK(n->prediction() == prediction);
    CHECK(n->default_prediction() == default_prediction);
    CHECK(n->lower_bound() == lower_bound);
    CHECK(n->objective() == objective);
    CHECK(n->num_captured() == (nsamples - num_not_captured));
    CHECK(n->depth() == (len_prefix + 1));
    CHECK(n->equivalent_minority() == equivalent_minority);
    CHECK_FALSE(n->deleted());
    CHECK(n->depth() == 1);

    tree->insert(n);

    // Root + this node = 2
    CHECK(tree->num_nodes() == 2);

    // Check heirarchy of tree
    CHECK(n->parent() == parent);
    CHECK(parent->children_begin()->second == n);
    CHECK(parent->num_children() == 1);
    CHECK(parent->child(rule_id) == n);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Check node delete behavior", "[trie][delete_node]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = tree->construct_node(1, nrules, true, true, 0.1, 0.12, root, 3, nsamples, 0, 0.01, 0.0);

    REQUIRE(n != NULL);

    tree->insert(n);

    // Check if the deleted behavior actually works
    n->set_deleted();
    CHECK(n->deleted());

    // Check if delete_child alters the tree correctly
    root->delete_child(1);

    CHECK(root->num_children() == 0);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Node get prefix and predictions", "[trie][node_prefix]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules - 1;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;
    tracking_vector<bool, DataStruct::Tree> predictions;

    // Create a nrules-deep tree and store its prefix and predictions
    for(int i = 0; i < depth; i++) {
        CAPTURE(i);
        n = tree->construct_node(i+1, nrules, (bool)(i % 2), true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);

        prefix.push_back(i+1);
        predictions.push_back((bool)(i % 2));
    }

    // depth is the number of nodes added, then add root
    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    std::pair<tracking_vector<unsigned short, DataStruct::Tree>, tracking_vector<bool, DataStruct::Tree>> p =
        n->get_prefix_and_predictions();

    // Check that the node correctly determines its prefix and predictions
    CHECK(p.first == prefix);
    CHECK(p.second == predictions);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Increment num evaluated", "[trie][num_evaluated]") {

    REQUIRE(tree != NULL);

    size_t num = tree->num_evaluated();
    tree->increment_num_evaluated();

    REQUIRE(tree->num_evaluated() == (num + 1));
}

TEST_CASE_METHOD(TrieFixture, "Trie/Decrement num nodes", "[trie][num_nodes]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = tree->construct_node(1, nrules, true, true, 0.1, 0.12, root, 3, nsamples, 0, 0.01, 0.0);

    REQUIRE(n != NULL);

    tree->insert(n);

    // Node + root
    REQUIRE(tree->num_nodes() == 2);

    tree->decrement_num_nodes();

    REQUIRE(tree->num_nodes() == 1);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Update minimum objective", "[trie][minimum_objective]") {

    REQUIRE(tree != NULL);

    double min0 = tree->min_objective();
    double min1 = min0 + 0.01;

    tree->update_min_objective(min1);

    REQUIRE(tree->min_objective() == min1);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Prune up", "[trie][prune_up]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules - 1;

    // Create one childless child of the root
    Node * s = tree->construct_node(2, nrules, true, true, 0.1, 0.12, n, 3, nsamples, 0, 0.01, 0.0);
    tree->insert(s);

    // Then create a deep line of nodes from another child of the root
    for(int i = 0; i < depth; i++) {
        CAPTURE(i);
        n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);
    }

    REQUIRE(tree->num_nodes() == (depth + 2));
    REQUIRE(n->depth() == depth);

    tree->prune_up(n);

    // Prune up should have deleted all the nodes with one child that are
    // ancestors of n, which does not include root (multiple children) or s (not an ancestor)
    CHECK(tree->num_nodes() == 2);

    tree->prune_up(s);

    // Pruning up s should have deleted s and root, so no more nodes
    CHECK(tree->num_nodes() == 0);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Check prefix", "[trie][check_prefix]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules - 1;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;

    for(int i = 0; i < depth; i++) {
        CAPTURE(i);
        n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);
        prefix.push_back(i+1);
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    // Check if the tree correctly finds a prefix
    CHECK(tree->check_prefix(prefix) == n);

    SECTION("Wrong rule") {

        // What if one of the prefix has a rule that isn't in the tree where it should be?
        prefix[depth - 1] += 1;
        CHECK(tree->check_prefix(prefix) == NULL);
    }

    SECTION("Not enough rules") {

        // What if the tree's not deep enough?
        n->parent()->delete_child(prefix[depth - 1]);
        CHECK(tree->check_prefix(prefix) == NULL);
    }
}

TEST_CASE_METHOD(TrieFixture, "Trie/Delete subtree", "[trie][delete_subtree]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules - 1;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;

    // This time, make two children of root, then from the left child make
    // two more, and from the left of those two make two more, etc for a certain depth
    for(int i = 0; i < depth; i++) {
        CAPTURE(i);

        // delete subtree requires the done information (interior nodes are 'done')
        n->set_done();

        Node * n1 = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        Node * n2 = tree->construct_node(i+2, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n1);
        tree->insert(n2);

        n = n1;

        prefix.push_back(i+1);
    }

    // each iteration of the for loop creates two nodes, and root
    REQUIRE(tree->num_nodes() == (2 * depth + 1));
    REQUIRE(tree->check_prefix(prefix) == n);

    REQUIRE(n->depth() == depth);

    // n is a leaf node
    REQUIRE_FALSE(n->done());

    // Get the child of root that has a big subtree under it
    Node * t = root->child(1);
    REQUIRE(t != NULL);
    REQUIRE(t->done());

    SECTION("Not destructive") {

        // Have to delete the node from its parent, since it isn't removed by delete_subtree
        root->delete_child(t->id());
        delete_subtree(tree, t, false, false);

        // Leaf nodes should be lazily marked, not deleted
        CHECK(n->deleted());
        // check_prefix should no longer find it, since most of it has been deleted
        CHECK(tree->check_prefix(prefix) == NULL);

        CHECK(tree->num_nodes() == (depth + 2));
    }

    SECTION("Destructive") {

        root->delete_child(t->id());
        delete_subtree(tree, t, true, false);

        // All deleted except root and its one childless child
        CHECK(tree->num_nodes() == 2);
    }

    SECTION("Full destructive") {

        delete_subtree(tree, root, true, false);

        // Everything's been deleted!
        CHECK(tree->num_nodes() == 0);

        // So the destructor of this fixture doesn't segfault
        tree->insert_root();
    }
}

TEST_CASE_METHOD(TrieFixture, "Trie/Update optimal rulelist", "[trie][optimal_rulelist]") {

    tracking_vector<unsigned short, DataStruct::Tree> rule_list = {0, 2, 1, 3};
    unsigned short new_rule = 5;
    tree->update_opt_rulelist(rule_list, new_rule);

    rule_list.push_back(new_rule);

    REQUIRE(tree->opt_rulelist() == rule_list);
}


TEST_CASE_METHOD(TrieFixture, "Trie/Update optimal predictions", "[trie][optimal_predictions]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    // Array of predictions for the line of nodes about to be created
    // (first child has false, child of that has true, child of that has false, etc.)
    tracking_vector<bool, DataStruct::Tree> predictions = {false, true, false};
    bool new_pred = false;
    bool new_default_pred = true;

    Node * n = root;
    int depth = predictions.size();

    for(int i = 0; i < depth; i++) {
        CAPTURE(i);

        n = tree->construct_node(i+1, nrules, predictions[i], true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    // This function should find the predictions of all its ancestors, plus new_pred (its prediction) and the default rule
    // Therefore it should get the same result as the predictions array used to create is ancestors
    tree->update_opt_predictions(n, new_pred, new_default_pred);

    // Plus these
    predictions.push_back(new_pred);
    predictions.push_back(new_default_pred);

    REQUIRE(tree->opt_predictions() == predictions);
}


TEST_CASE_METHOD(TrieFixture, "Trie/Garbage collect", "[trie][garbage_collect]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    double minobj = 0.5;
    tree->update_min_objective(minobj);
    REQUIRE(tree->min_objective() == minobj);

    // We create three children from the root node. In order:
    // higher, equal, and lower lower bound than the minimum objective (0.5).
    // Each one has two children.

    Node * nodes[3][3];

    nodes[0][0] = tree->construct_node(1, nrules, true, true, minobj + 0.2, 0.12, root, 3, nsamples, 0, 0.01, 0.0);
    nodes[1][0] = tree->construct_node(2, nrules, true, true, minobj, 0.12, root, 3, nsamples, 0, 0.01, 0.0);
    nodes[2][0] = tree->construct_node(3, nrules, true, true, minobj - 0.2, 0.12, root, 3, nsamples, 0, 0.01, 0.0);

    root->set_done();

    for(int i = 0; i < 3; i++) {
        CAPTURE(i);

        nodes[i][0]->set_done();
        tree->insert(nodes[i][0]);

        nodes[i][1] = tree->construct_node(4, nrules, true, true, minobj - 0.1, 0.12, nodes[i][0], 3, nsamples, 1, 0.01, 0.0);
        nodes[i][2] = tree->construct_node(5, nrules, true, true, minobj - 0.15, 0.12, nodes[i][0], 3, nsamples, 1, 0.01, 0.0);

        tree->insert(nodes[i][1]);
        tree->insert(nodes[i][2]);
    }

    // Check if all the nodes were counted
    CHECK(tree->num_nodes() == 10);

    tree->garbage_collect();

    // The first and second nodes (higher and equal lower bounds) should have been deleted
    CHECK(tree->num_nodes() == 8);

    // And their childeren lazily marked
    CHECK(nodes[0][1]->deleted());
    CHECK(nodes[0][2]->deleted());
    CHECK(nodes[1][1]->deleted());
    CHECK(nodes[1][2]->deleted());

    // But not the third node's children (lower lower bound)
    CHECK_FALSE(nodes[2][1]->deleted());
    CHECK_FALSE(nodes[2][2]->deleted());

    // Just for fun, add a test for the queue lazy cleanup (where it deletes nodes marked for deletion)
    Queue * queue = new Queue(lb_cmp, "LOWER BOUND");

    REQUIRE(queue != NULL);

    // Add all the leaf nodes that need to be deleted to the queue
    for(int i = 0; i < 2; i++) {
        queue->push(nodes[i][1]);
        queue->push(nodes[i][2]);
    }

    VECTOR captured;
    rule_vinit(nsamples, &captured);

    std::pair<Node*, tracking_vector<unsigned short, DataStruct::Tree>> prefix_node = queue->select(tree, captured);

    // Were all the nodes found to be lazily marked deleted?
    // Only the root, the root's third child and its two children should remain
    CHECK(tree->num_nodes() == 4);

    // Since all the nodes in the queue were deleted
    CHECK(prefix_node.first == NULL);

    rule_vfree(&captured);
}


TEST_CASE_METHOD(PrefixMapFixture, "Prefix Map/Insert into empty map", "[prefixmap][insert_empty][prefix_empty]") {

    REQUIRE(pmap != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                            lower_bound, objective, root, num_not_captured,
                            nsamples, len_prefix, c, equivalent_minority, tree,
                            NULL, parent_prefix);

    REQUIRE(n != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    PrefixMap::iterator inserted = pmap->getMap()->begin();

    // Is inserted a valid pointer?
    REQUIRE(inserted != pmap->getMap()->end());

    // Check if the lower bound was recorded correctly
    CHECK(inserted->second.first == lower_bound);

    unsigned short* key = inserted->first.key;
    unsigned char* indices = inserted->second.second;

    CHECK(key[0] == indices[0]);
    CHECK(key[0] == len_prefix);

    // Check if the inserted key and indices are correct
    for(int i = 0; i < len_prefix+1; i++) {
        CAPTURE(i);
        CHECK(key[i] == correct_key.at(i));
        CHECK(indices[i] == correct_indices.at(i));
    }

    // Check if the node was created correctly
    CHECK(n->parent() == root);
    CHECK(n->prediction() == prediction);
    CHECK(n->default_prediction() == default_prediction);
    CHECK(n->lower_bound() == lower_bound);
    CHECK(n->objective() == objective);
    CHECK(n->num_captured() == (nsamples - num_not_captured));
    CHECK(n->equivalent_minority() == equivalent_minority);
}

TEST_CASE_METHOD(PrefixMapFixture, "Prefix Map/Insert with higher lower bound", "[prefixmap][insert_higher][prefix_higher]") {

    REQUIRE(pmap != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                            lower_bound, objective, root, num_not_captured,
                            nsamples, len_prefix, c, equivalent_minority, tree,
                            NULL, parent_prefix);

    REQUIRE(n != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    double h_bound = lower_bound + 0.02;

    // Expected behavior is that the map remains unchanged, since h_bound
    // is greated than lower_bound
    Node * n2 = pmap->insert(new_rule_2, nrules, prediction, default_prediction,
                             h_bound, objective, root, num_not_captured,
                             nsamples, len_prefix, c, equivalent_minority, tree,
                             NULL, parent_prefix_2);

    REQUIRE(n2 == NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    PrefixMap::iterator inserted = pmap->getMap()->begin();

    REQUIRE(inserted != pmap->getMap()->end());

    unsigned short* key = inserted->first.key;
    unsigned char* indices = inserted->second.second;

    CHECK(key[0] == indices[0]);
    CHECK(key[0] == len_prefix);

    // Check if the key and indices are unchanged (same as the ones inserted with n instead of n2)
    for(int i = 0; i < len_prefix+1; i++) {
        CAPTURE(i);
        CHECK(key[i] == correct_key.at(i));
        CHECK(indices[i] == correct_indices.at(i));
    }

    // Check if the node wasn't inserted (it should not have, since the permutation bound should block it)
    CHECK(n2 == NULL);

    // Check if the lower bound is unchanged
    CHECK(inserted->second.first == lower_bound);
}

TEST_CASE_METHOD(PrefixMapFixture, "Prefix Map/Insert with lower lower bound", "[prefixmap][insert_lower][prefix_lower]") {

    REQUIRE(pmap != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                            lower_bound, objective, root,
                            0, nsamples, len_prefix, c, 0.0, tree, NULL,
                            parent_prefix);

    REQUIRE(n != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    double l_bound = lower_bound - 0.02;

    // Expected behavior is that the map will change the indices
    // and update the best permutation
    Node * n2 = pmap->insert(new_rule_2, nrules, prediction, default_prediction,
                             l_bound, objective, root, num_not_captured,
                             nsamples, len_prefix, c, equivalent_minority, tree,
                             NULL, parent_prefix_2);

    REQUIRE(n2 != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    PrefixMap::iterator inserted = pmap->getMap()->begin();

    REQUIRE(inserted != pmap->getMap()->end());

    unsigned short* key = inserted->first.key;
    unsigned char* indices = inserted->second.second;

    CHECK(key[0] == indices[0]);
    CHECK(key[0] == len_prefix);

    // Check if the indices are changed and are correct (new values)
    for(int i = 0; i < len_prefix+1; i++) {
        CAPTURE(i);
        CHECK(key[i] == correct_key.at(i));
        CHECK(indices[i] == correct_indices_2.at(i));
    }

    // Check if the lower bound is the new correct lower bound
    CHECK(inserted->second.first == l_bound);
}

TEST_CASE_METHOD(CapturedMapFixture, "Captured Map/Insert into empty map", "[capturemap][insert_empty][capture_empty]") {

    REQUIRE(pmap != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                            lower_bound, objective, root, num_not_captured,
                            nsamples, len_prefix, c, equivalent_minority, tree,
                            not_captured, parent_prefix);

    REQUIRE(n != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    CapturedMap::iterator inserted = pmap->getMap()->begin();

    // Is inserted a valid pointer?
    CHECK(inserted != pmap->getMap()->end());

    // Check if the lower bound was recorded correctly
    CHECK(inserted->second.first == lower_bound);

    // Check if the key is correct
#ifdef GMP
    CHECK(mpz_cmp(inserted->first.key, not_captured) == 0);
#else
    for(int i = 0; i < NENTRIES; i++) {
        CAPTURE(i);
        CHECK(inserted->first.key[i] == not_captured[i]);
    }
#endif

    parent_prefix.push_back(new_rule);
    CHECK(inserted->second.second == parent_prefix);

    // Check if the node was created correctly
    CHECK(n->parent() == root);
    CHECK(n->prediction() == prediction);
    CHECK(n->default_prediction() == default_prediction);
    CHECK(n->lower_bound() == lower_bound);
    CHECK(n->objective() == objective);
    CHECK(n->num_captured() == (nsamples - num_not_captured));
    CHECK(n->equivalent_minority() == equivalent_minority);

}

TEST_CASE_METHOD(CapturedMapFixture, "Captured Map/Insert with higher lower bound", "[capturemap][insert_higher][capture_higher]") {

    REQUIRE(pmap != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                            lower_bound, objective, root, num_not_captured,
                            nsamples, len_prefix, c, equivalent_minority, tree,
                            not_captured, parent_prefix);

    REQUIRE(n != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    double h_bound = lower_bound + 0.02;

    // Expected behavior is that the map remains unchanged, since h_bound
    // is greated than lower_bound
    Node * n2 = pmap->insert(new_rule_2, nrules, prediction, default_prediction,
                             h_bound, objective, root, num_not_captured,
                             nsamples, len_prefix, c, equivalent_minority, tree,
                             not_captured, parent_prefix_2);

    REQUIRE(pmap->getMap()->size() == 1);

    CapturedMap::iterator inserted = pmap->getMap()->begin();

    CHECK(inserted != pmap->getMap()->end());

    // Check if the key is the same as always
#ifdef GMP
    CHECK(mpz_cmp(inserted->first.key, not_captured) == 0);
#else
    for(int i = 0; i < NENTRIES; i++) {
        CAPTURE(i);
        CHECK(inserted->first.key[i] == not_captured[i]);
    }
#endif

    // Check if the prefix is the same as the first node, since the second node should have been blocked by the permutation bound
    parent_prefix.push_back(new_rule);
    CHECK(inserted->second.second == parent_prefix);

    // Check if the node wasn't inserted (it should not have, since the permutation bound should block it)
    CHECK(n2 == NULL);

    // Check if the lower bound is unchanged
    CHECK(inserted->second.first == lower_bound);
}

TEST_CASE_METHOD(CapturedMapFixture, "Captured Map/Insert with lower lower bound", "[capturemap][insert_lower][capture_lower]") {

    REQUIRE(pmap != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = pmap->insert(new_rule, nrules, prediction, default_prediction,
                            lower_bound, objective, root, num_not_captured,
                            nsamples, len_prefix, c, equivalent_minority, tree,
                            not_captured, parent_prefix);

    REQUIRE(n != NULL);
    REQUIRE(pmap->getMap()->size() == 1);

    double l_bound = lower_bound - 0.02;

    // Expected behavior is that the map will change the indices
    // and update the best permutation
    Node * n2 = pmap->insert(new_rule_2, nrules, prediction, default_prediction,
                             l_bound, objective, root, num_not_captured,
                             nsamples, len_prefix, c, equivalent_minority, tree,
                             not_captured, parent_prefix_2);

    REQUIRE(pmap->getMap()->size() == 1);

    CapturedMap::iterator inserted = pmap->getMap()->begin();

    CHECK(inserted != pmap->getMap()->end());

    // Check if the key is the same
#ifdef GMP
    CHECK(mpz_cmp(inserted->first.key, not_captured) == 0);
#else
    for(int i = 0; i < NENTRIES; i++) {
        CAPTURE(i);
        CHECK(inserted->first.key[i] == not_captured[i]);
    }
#endif

    // Check if the prefix has been updated to the new best lower bound (the second prefix)
    parent_prefix_2.push_back(new_rule_2);
    CHECK(inserted->second.second == parent_prefix_2);

    // Check if the node was inserted
    CHECK(n2 != NULL);

    // Check if the lower bound is the new correct lower bound
    CHECK(inserted->second.first == l_bound);
}

TEST_CASE_METHOD(QueueFixture, "Queue/Push and Front", "[queue][push]") {

    REQUIRE(queue != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    queue->push(root);

    CHECK_FALSE(queue->empty());
    CHECK(queue->size() == 1);
    CHECK(queue->front() == root);
}

TEST_CASE_METHOD(QueueFixture, "Queue/Pop", "[queue][pop]") {

    REQUIRE(queue != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    queue->push(root);
    CHECK(queue->size() == 1);

    queue->pop();
    CHECK(queue->empty());
    CHECK(queue->size() == 0);
}

TEST_CASE_METHOD(QueueFixture, "Queue/Select", "[queue][select]") {

    REQUIRE(queue != NULL);
    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    REQUIRE(tree->nsamples() == nsamples);
    REQUIRE(tree->nrules() == nrules);

    Node * n = root;
    int depth = nrules - 1;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;

    // Vector of captured samples
    VECTOR captured_key;
    rule_vinit(nsamples, &captured_key);

    // As before, create a line of nodes
    for(int i = 0; i < depth; i++) {
        CAPTURE(i);

        n->set_done();
        n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);

        prefix.push_back(i+1);

        // Here, we generated the vector of captured samples to then test against what the queue calculates
#ifdef GMP
        mpz_ior(captured_key, captured_key, rules[i+1].truthtable);
#else
        for(int j = 0; j < NENTRIES; j++) {
            CAPTURE(j);
            captured_key[j] = captured_key[j] | rules[i+1].truthtable[j];
        }
#endif
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    // Add n to the queue so we can select it
    queue->push(n);
    REQUIRE(queue->front() == n);

    VECTOR captured;
    rule_vinit(nsamples, &captured);

    // Test if selected a node returns it and its data correctly
    SECTION("Test select normal") {

        std::pair<Node*, tracking_vector<unsigned short, DataStruct::Tree>> prefix_node = queue->select(tree, captured);

        // Did it get the correct node from the queue?
        CHECK(prefix_node.first == n);

        // Did it get the node's correct prefix?
        CHECK(prefix_node.second == prefix);

        // Did it get the correct captured vector?
#ifdef GMP
        CHECK(mpz_cmp(captured, captured_key) == 0);
#else
        for(int i = 0; i < NENTRIES; i++) {
            CAPTURE(i);
            CHECK(captured[i] == captured_key[i]);
        }
#endif
    }

    // Test if selecting a node that is lazily marked deletes it and returns null
    SECTION("Test select lazy delete cleanup") {

        Node * t = root->child(1);
        REQUIRE(t != NULL);
        REQUIRE(t->done());

        // Instead of just setting n to deleted, make it with the delete_subtree function (as an extra check for the trie)
        root->delete_child(t->id());
        delete_subtree(tree, t, false, false);

        CHECK(tree->num_nodes() == 2);

        // Leaf nodes should be lazily marked, not deleted
        CHECK(n->deleted());

        std::pair<Node*, tracking_vector<unsigned short, DataStruct::Tree>> prefix_node = queue->select(tree, captured);

        // Was the node found to be lazily marked and deleted?
        CHECK(prefix_node.first == NULL);
        CHECK(tree->num_nodes() == 1);

        // Is captured empty?
#ifdef GMP
        mpz_t temp;
        mpz_init2(temp, nsamples);

        CHECK(mpz_cmp(captured, temp) == 0);

        mpz_clear(temp);
#else
        for(int i = 0; i < NENTRIES; i++) {
            CAPTURE(i);
            CHECK(captured[i] == 0);
        }
#endif
    }

    rule_vfree(&captured);
    rule_vfree(&captured_key);
}
