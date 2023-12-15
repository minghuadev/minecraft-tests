
#include <time.h>
#include <sys/random.h>
#include <openssl/evp.h>

#define PT_LEN (63 * 1024)
#define CT_LEN PT_LEN
#define IV_LEN 16
#define KEY_LEN 16
#define ITER_COUNT 100000

static uint8_t pt[PT_LEN];
static uint8_t ct[CT_LEN];
static uint8_t key[KEY_LEN];
static uint8_t iv[IV_LEN];

static void time_diff(struct timespec *res, const struct timespec *start, const struct timespec *end)
{
    res->tv_sec = end->tv_sec - start->tv_sec;
    res->tv_nsec = end->tv_nsec - start->tv_nsec;
    if (res->tv_nsec < 0) {
        res->tv_sec--;
        res->tv_nsec += 1000000000;
    }
}

int main(void)
{
    // Fill the test data
    getrandom(key, sizeof(key), GRND_NONBLOCK);
    getrandom(iv, sizeof(iv), GRND_NONBLOCK);
    getrandom(pt, sizeof(pt), GRND_NONBLOCK);

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_aes_128_ctr(), NULL, key, iv);

    int outl = sizeof(ct);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    int i;
    for (i = 0; i < ITER_COUNT; i++) {
        EVP_EncryptUpdate(ctx, ct, &outl, pt, sizeof(pt));
    }
    uint8_t *ct_final = ct + outl;
    outl = sizeof(ct) - outl;
    EVP_EncryptFinal_ex(ctx, ct_final, &outl);

    clock_gettime(CLOCK_MONOTONIC, &end);

    EVP_CIPHER_CTX_free(ctx);

    struct timespec diff;
    time_diff(&diff, &start, &end);
    double tput_ossl = ((double)ITER_COUNT * PT_LEN) / (diff.tv_sec + (diff.tv_nsec * 0.000000001 ));
    printf("OpenSSL: %.02f Mb/s\n", tput_ossl / (1024 * 1024));

    return 0;
}


