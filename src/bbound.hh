#include "cache.hh"
#include <functional>
#include <queue>
#include <map>
#include <unordered_map>
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

// lambda function for priority queue metric using objective as curiosity
auto objective_cmp = [](CuriousNode* left, CuriousNode* right) {
    return left->objective() > right->objective();
};

// lambda function for priority queue metric implementing depth-first
auto depth_first_cmp = [](CuriousNode* left, CuriousNode* right) {
    return left->depth() < right->depth();
};

typedef std::priority_queue<CuriousNode*, std::vector<CuriousNode*>,
                            std::function<bool(CuriousNode*, CuriousNode*)> > CuriousQueue;

BaseNode* base_queue_front(BaseQueue* q);

CuriousNode* curious_queue_front(CuriousQueue* q);

template<class N>
using construct_signature = N* (*)(unsigned short, size_t, bool, bool, double, double,
                                   N* parent, int, int, int, double, double);

BaseNode* base_construct_policy(unsigned short new_rule, size_t nrules,
                                bool prediction, bool default_prediction,
                                double lower_bound, double objective,
                                BaseNode* parent, int num_not_captured,
                                int nsamples, int len_prefix, double c, double minority);

CuriousNode* curious_construct_policy(unsigned short new_rule, size_t nrules,
                                      bool prediction, bool default_prediction,
                                      double lower_bound, double objective,
                                      CuriousNode* parent, int num_not_captured,
                                      int nsamples, int len_prefix, double c, double minority);

/*
 * Permutation Map
 */
/*struct cmpVECTOR {
    bool operator()(const VECTOR& left, const VECTOR& right) const {
        return *left < *right;
    }
};*/

struct prefix_key {
    unsigned short *key;

    bool operator==(const prefix_key& other) const {
        if (key[0] != other.key[0])
            return false;
        for(size_t i = 1; i <= *key; ++i) {
            if (key[i] != other.key[i])
                return false;
        }
        return true;
    }
};

struct prefix_hash {
    std::size_t operator()(const prefix_key& k) const {
        unsigned long hash = 0;
        for(size_t i = 1; i <= *k.key; ++i)
            hash = k.key[i] + (hash << 6) + (hash << 16) - hash;
        return hash;
    }
};

/*struct prefix_value {
    bool is_lb;
    union {
        double lower_bound;
        unsigned char* indices;
    } v;
};*/

struct captured_key {
    VECTOR key;

    bool operator==(const captured_key& other) const {
#ifdef GMP
        return !mpz_cmp(other.key, key);
#else
        return false;
#endif
    }
};

struct captured_hash {
    std::size_t operator()(const captured_key& k) const{
        unsigned long hash = 0;
#ifdef GMP
        for(size_t i = 0; i < mpz_size(k.key); ++i)
            hash = mpz_getlimbn(k.key, i) + (hash << 6) + (hash << 16) - hash;
#endif
        return hash;
    }
};

//typedef std::vector<bool> CapturedKey;
//typedef VECTOR CapturedKey;
typedef std::unordered_map<struct prefix_key, std::pair<double, unsigned char*>, prefix_hash> PrefixPermutationMap;
//typedef std::unordered_map<struct prefix_key, struct prefix_value, prefix_hash> PrefixPermutationMap;
typedef std::unordered_map<struct captured_key, std::pair<std::vector<unsigned short>, double>, captured_hash> CapturedPermutationMap;

template<class P>
using pmap_garbage_collect_signature = void (*)(P*, size_t);

void bfs_prefix_map_garbage_collect(PrefixPermutationMap* p, size_t min_length);
void prefix_map_garbage_collect(PrefixPermutationMap* p, size_t min_length);
void captured_map_garbage_collect(CapturedPermutationMap* p, size_t min_length);

template<class N, class P>
using permutation_insert_signature = N* (*)(construct_signature<N>, unsigned short, size_t, bool, bool, 
                                            double, double, N* parent, int, int, int, double, double, CacheTree<N>*, VECTOR,
                                            std::vector<unsigned short>, P*);

template<class N>
N* prefix_permutation_insert(construct_signature<N> construct_policy, unsigned short new_rule,
                        size_t nrules, bool prediction, bool default_prediction, double lower_bound,
                        double objective, N* parent, int num_not_captured, int nsamples, int len_prefix,
                        double c, double minority, CacheTree<N>* tree, VECTOR not_captured,
                        std::vector<unsigned short>, PrefixPermutationMap* p);

template<class N>
N* captured_permutation_insert(construct_signature<N> construct_policy, unsigned short new_rule,
                        size_t nrules, bool prediction, bool default_prediction, double lower_bound,
                        double objective, N* parent, int num_not_captured, int nsamples, int len_prefix,
                        double c, double minority, CacheTree<N>* tree, VECTOR not_captured,
                        std::vector<unsigned short>, CapturedPermutationMap* p);

template<class N>
extern N* stochastic_select(CacheTree<N>* tree, VECTOR not_captured);

template<class N, class P>
extern void bbound_stochastic(CacheTree<N>* tree,
                              size_t max_num_nodes,
                              construct_signature<N> construct_policy,
                              permutation_insert_signature<N, P> permutation_insert,
                              pmap_garbage_collect_signature<P> pmap_garbage_collect,
                              P* p);

template<class N, class Q>
extern N*
queue_select(CacheTree<N>* tree, Q* q, N*(*front)(Q*), VECTOR captured);

template<class N, class Q, class P>
extern int bbound_queue(CacheTree<N>* tree,
                         size_t max_num_nodes,
                         construct_signature<N> construct_policy,
                         Q* q, N*(*front)(Q*),
                         permutation_insert_signature<N, P> permutation_insert,
                         pmap_garbage_collect_signature<P> pmap_garbage_collect,
                         P* p, size_t num_iter, size_t switch_iter);

template<class N, class Q, class P>
extern void evaluate_children(CacheTree<N>* tree, N* parent,
                              VECTOR parent_not_captured,
                              construct_signature<N> construct_policy,
                              Q* q,
                              permutation_insert_signature<N, P> permutation_insert,
                              P* p);

template<class N>
extern void delete_subtree(CacheTree<N>* tree, N* node, bool destructive, bool update_remaining_state_space);

void bbound_greedy(size_t nsamples, size_t nrules, rule_t *rules, rule_t *labels, size_t max_prefix_length);
