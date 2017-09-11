#include <sys/time.h>
#include <stdlib.h>
#include <stdio.h>
#include <gmp.h>

__global__ void Kernel(mp_limb_t *rule_a, mp_limb_t *rule_b, mp_limb_t *rule_c, int nentries)
{
	int i = blockDim.x * blockIdx.x + threadIdx.x;

	if(i < nentries)
	   rule_c[i] = rule_a[i] & rule_b[i];
}

inline double timestamp()
{
	struct timeval now;
	gettimeofday(&now, 0);
	return now.tv_sec + now.tv_usec * 0.000001;
}

inline void randomize_vector(mpz_t v, int nsamples, gmp_randstate_t state)
{
    mpz_rrandomb(v, state, nsamples);
}

int main()
{
	double t0 = timestamp();

    gmp_randstate_t rand_state;
    gmp_randinit_mt(rand_state);

	mpz_t rule_a, rule_b, rule_c, cuda_rule_c;
    int nsamples = 100000000;
	mpz_init2(rule_a, nsamples);
    mpz_init2(rule_b, nsamples);
    mpz_init2(rule_c, nsamples);
    mpz_init2(cuda_rule_c, nsamples);
    randomize_vector(rule_a, nsamples, rand_state);
    randomize_vector(rule_b, nsamples, rand_state);

    double t1 = timestamp();

    int nentries = abs(rule_a->_mp_size);

    mp_limb_t *d_rule_a, *d_rule_b, *d_rule_c;
    size_t s = nentries * sizeof(mp_limb_t);

	cudaMalloc(&d_rule_a, s);
	cudaMalloc(&d_rule_b, s);
	cudaMalloc(&d_rule_c, s);

	cudaMemcpy(d_rule_a, rule_a->_mp_d, s, cudaMemcpyHostToDevice);
	cudaMemcpy(d_rule_b, rule_b->_mp_d, s, cudaMemcpyHostToDevice);

	int threadsPerBlock = 256;
	int blocksPerGrid = (nentries + threadsPerBlock - 1) / threadsPerBlock;
	dim3 blocks(blocksPerGrid, 1, 1);
	dim3 threads(threadsPerBlock, 1, 1);

	double t2 = timestamp();

	Kernel<<<blocks, threads>>>(d_rule_a, d_rule_b, d_rule_c, nentries);
	cudaThreadSynchronize();

	double t3 = timestamp();

	cudaMemcpy(cuda_rule_c->_mp_d, d_rule_c, s, cudaMemcpyDeviceToHost);

	cudaFree(d_rule_a);
	cudaFree(d_rule_b);
	cudaFree(d_rule_c);

    double t4 = timestamp();

    mpz_and(rule_c, rule_a, rule_b);

    double t5 = timestamp();

    cuda_rule_c->_mp_size = rule_c->_mp_size;

	mpz_clear(rule_a);
	mpz_clear(rule_b);
	mpz_clear(rule_c);
    mpz_clear(cuda_rule_c);

    double t6 = timestamp();

    if(mpz_cmp(rule_c, cuda_rule_c) == 0) {
        printf("Outputs match!\n");
    }

	printf("\n\nSetup time: %.8f\n", t1 - t0);
    printf("CUDA kernel run time: %.8f\n", t3 - t2);
    printf("CUDA total run time: %.8f\n", t4 - t1);
    printf("GMP total run time: %.8f\n", t5 - t4);
    printf("Total time: %.8f\n", t6 - t0);

	return 0;
}
