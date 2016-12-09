#include "cache.hh"
#include <functional>
#include <queue>
#include <map>
#include <set>

/*
 * Queue
 */

template<class N>
class NullQueue {
  public:
    void push(N*) {};
    size_t size() {return 0;};
};

typedef std::queue<BaseNode*> BaseQueue;

// lambda function for priority queue metric using curiosity
auto curious_cmp = [](CuriousNode* left, CuriousNode* right) {
    return left->get_storage() > right->get_storage();
};

// lambda function for priority queue metric using lower bound as curiosity
auto lower_bound_cmp = [](CuriousNode* left, CuriousNode* right) {
    return left->lower_bound() > right->lower_bound();
};

typedef std::priority_queue<CuriousNode*, std::vector<CuriousNode*>,
                            std::function<bool(CuriousNode*, CuriousNode*)> > CuriousQueue;

BaseNode* base_queue_front(BaseQueue* q);

CuriousNode* curious_queue_front(CuriousQueue* q);

template<class N>
using construct_signature = N* (*)(size_t, size_t, bool, bool, double, double,
                                   N* parent, int, int, int, double);

BaseNode* base_construct_policy(size_t new_rule, size_t nrules,
                                bool prediction, bool default_prediction,
                                double lower_bound, double objective,
                                BaseNode* parent, int num_not_captured,
                                int nsamples, int len_prefix, double c);

CuriousNode* curious_construct_policy(size_t new_rule, size_t nrules,
                                      bool prediction, bool default_prediction,
                                      double lower_bound, double objective,
                                      CuriousNode* parent, int num_not_captured,
                                      int nsamples, int len_prefix, double c);

/*
 * Permutation Map
 */
typedef std::set<size_t> PrefixKey;
typedef std::vector<bool> CapturedKey;
typedef std::map<PrefixKey, std::pair<std::vector<size_t>, double> > PrefixPermutationMap;
typedef std::map<CapturedKey, std::pair<std::vector<size_t>, double> > CapturedPermutationMap;

template<class P>
using pmap_garbage_collect_signature = void (*)(P*, size_t);

void bfs_prefix_map_garbage_collect(PrefixPermutationMap* p, size_t min_length);
void prefix_map_garbage_collect(PrefixPermutationMap* p, size_t min_length);
void captured_map_garbage_collect(CapturedPermutationMap* p, size_t min_length);

template<class N, class P>
using permutation_insert_signature = N* (*)(construct_signature<N>, size_t, size_t, bool, bool, 
                                            double, double, N* parent, int, int, int, double, CacheTree<N>*, VECTOR,
                                            std::vector<size_t>, P*);

template<class N>
N* prefix_permutation_insert(construct_signature<N> construct_policy, size_t new_rule,
                        size_t nrules, bool prediction, bool default_prediction, double lower_bound,
                        double objective, N* parent, int num_not_captured, int nsamples, int len_prefix,
                        double c, CacheTree<N>* tree, VECTOR not_captured, std::vector<size_t>, PrefixPermutationMap* p);

template<class N>
N* captured_permutation_insert(construct_signature<N> construct_policy, size_t new_rule,
                        size_t nrules, bool prediction, bool default_prediction, double lower_bound,
                        double objective, N* parent, int num_not_captured, int nsamples, int len_prefix,
                        double c, CacheTree<N>* tree, VECTOR not_captured, std::vector<size_t>, CapturedPermutationMap* p);

template<class N, class P>
extern std::pair<N*, std::set<size_t> > stochastic_select(CacheTree<N>* tree, VECTOR not_captured, P* p);

template<class N>
extern void bbound_stochastic(CacheTree<N>* tree,
                              size_t max_num_nodes,
                              construct_signature<N> construct_policy);

template<class N, class Q>
extern std::pair<N*, std::set<size_t> >
queue_select(CacheTree<N>* tree, Q* q, N*(*front)(Q*), VECTOR captured);

template<class N, class Q, class P>
extern void bbound_queue(CacheTree<N>* tree,
                         size_t max_num_nodes,
                         construct_signature<N> construct_policy,
                         Q* q, N*(*front)(Q*),
                         permutation_insert_signature<N, P> permutation_insert,
                         pmap_garbage_collect_signature<P> pmap_garbage_collect,
                         P* p);

template<class N, class Q, class P>
extern void evaluate_children(CacheTree<N>* tree, N* parent,
                              VECTOR parent_not_captured,
                              std::set<size_t> ordered_parent,
                              construct_signature<N> construct_policy,
                              Q* q,
                              permutation_insert_signature<N, P> permutation_insert,
                              P* p);

template<class N>
extern void delete_subtree(CacheTree<N>* tree, N* node, bool destructive);

void bbound_greedy(size_t nsamples, size_t nrules, rule_t *rules, rule_t *labels, size_t max_prefix_length);
