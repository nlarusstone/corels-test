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

    CHECK(tree->num_nodes() == 2);

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

    n->set_deleted();
    CHECK(n->deleted());

    root->delete_child(1);

    CHECK(root->num_children() == 0);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Node get prefix and predictions", "[trie][node_prefix]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;
    tracking_vector<bool, DataStruct::Tree> predictions;

    for(int i = 0; i < depth; i++) {
        n = tree->construct_node(i+1, nrules, (bool)(i % 2), true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);

        prefix.push_back(i+1);
        predictions.push_back((bool)(i % 2));
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    std::pair<tracking_vector<unsigned short, DataStruct::Tree>, tracking_vector<bool, DataStruct::Tree>> p =
        n->get_prefix_and_predictions();

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
    int depth = nrules;

    Node * s = tree->construct_node(2, nrules, true, true, 0.1, 0.12, n, 3, nsamples, 0, 0.01, 0.0);
    tree->insert(s);

    for(int i = 0; i < depth; i++) {
        n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);
    }

    REQUIRE(tree->num_nodes() == (depth + 2));
    REQUIRE(n->depth() == depth);

    tree->prune_up(n);

    CHECK(tree->num_nodes() == 2);

    tree->prune_up(s);

    CHECK(tree->num_nodes() == 0);
}

TEST_CASE_METHOD(TrieFixture, "Trie/Check prefix", "[trie][check_prefix]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules - 1;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;

    for(int i = 0; i < depth; i++) {
        n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);
        prefix.push_back(i+1);
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    CHECK(tree->check_prefix(prefix) == n);

    SECTION("Wrong rule") {

        prefix[depth - 1] += 1;
        CHECK(tree->check_prefix(prefix) == NULL);
    }

    SECTION("Not enough rules") {
        n->parent()->delete_child(prefix[depth - 1]);
        CHECK(tree->check_prefix(prefix) == NULL);
    }
}

TEST_CASE_METHOD(TrieFixture, "Trie/Delete subtree", "[trie][delete_subtree]") {

    REQUIRE(tree != NULL);
    REQUIRE(root != NULL);

    Node * n = root;
    int depth = nrules;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;

    for(int i = 0; i < depth; i++) {
        n->set_done();

        Node * n1 = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        Node * n2 = tree->construct_node(i+2, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n1);
        tree->insert(n2);

        n = n1;

        prefix.push_back(i+1);
    }

    REQUIRE(tree->num_nodes() == (2 * depth + 1));
    REQUIRE(tree->check_prefix(prefix) == n);

    REQUIRE(n->depth() == depth);
    REQUIRE_FALSE(n->done());

    Node * t = root->child(1);
    REQUIRE(t != NULL);
    REQUIRE(t->done());

    SECTION("Not destructive") {

        root->delete_child(t->id());
        delete_subtree(tree, t, false, false);

        CHECK(n->deleted());
        CHECK(tree->check_prefix(prefix) == NULL);

        CHECK(tree->num_nodes() == (depth + 2));
    }

    SECTION("Destructive") {

        root->delete_child(t->id());
        delete_subtree(tree, t, true, false);

        CHECK(tree->num_nodes() == 2);
    }

    SECTION("Full destructive") {

        delete_subtree(tree, root, true, false);

        CHECK(tree->num_nodes() == 0);

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

    tracking_vector<bool, DataStruct::Tree> predictions = {false, true, false};
    bool new_pred = false;
    bool new_default_pred = true;

    Node * n = root;
    int depth = predictions.size();

    for(int i = 0; i < depth; i++) {
        n = tree->construct_node(i+1, nrules, predictions[i], true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    tree->update_opt_predictions(n, new_pred, new_default_pred);

    predictions.push_back(new_pred);
    predictions.push_back(new_default_pred);

    REQUIRE(tree->opt_predictions() == predictions);
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

    // Check if the key is the same
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
    int depth = nrules;

    tracking_vector<unsigned short, DataStruct::Tree> prefix;

    VECTOR captured_key;
    rule_vinit(nsamples, &captured_key);

    for(int i = 0; i < depth; i++) {
        n = tree->construct_node(i+1, nrules, true, true, 0.1, 0.12, n, 3, nsamples, i, 0.01, 0.0);
        tree->insert(n);

        prefix.push_back(i+1);

#ifdef GMP
        mpz_ior(captured_key, captured_key, rules[i+1].truthtable);
#else
        for(int j = 0; j < NENTRIES; j++) {
            captured_key[j] = captured_key[j] | rules[i+1].truthtable[j];
        }
#endif
    }

    REQUIRE(tree->num_nodes() == (depth + 1));
    REQUIRE(n->depth() == depth);

    queue->push(n);
    REQUIRE(queue->front() == n);

    VECTOR captured;
    rule_vinit(nsamples, &captured);

    std::pair<Node*, tracking_vector<unsigned short, DataStruct::Tree>> prefix_node = queue->select(tree, captured);

    CHECK(prefix_node.first == n);

    CHECK(prefix_node.second == prefix);

#ifdef GMP
    CHECK(mpz_cmp(captured, captured_key) == 0);
#else
    for(int i = 0; i < NENTRIES; i++) {
        CHECK(captured[i] == captured_key[i]);
    }
#endif

    rule_vfree(&captured);
    rule_vfree(&captured_key);
}
