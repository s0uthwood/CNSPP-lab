#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define ROL(a, b) ((a << b) | (a >> (32 - b)))
#define QUARTERROUND(x, a, b, c, d) \
    x[a] += x[b]; x[d] ^= x[a]; ROL(x[d], 16); \
    x[c] += x[d]; x[b] ^= x[c]; ROL(x[b], 12); \
    x[a] += x[b]; x[d] ^= x[a]; ROL(x[d],  8);  \
    x[c] += x[d]; x[b] ^= x[c]; ROL(x[b],  7);

void chacha20_corn(uint32_t *in, uint32_t *out){
    for (int i = 0; i < 16; i++)
        out[i] = in[i];
    for (int i = 0; i < 10; i++){
        QUARTERROUND(out,  0,  4,  8, 12);
        QUARTERROUND(out,  1,  5,  9, 13);
        QUARTERROUND(out,  2,  6, 10, 14);
        QUARTERROUND(out,  3,  7, 11, 15);

        QUARTERROUND(out,  0,  5, 10, 15);
        QUARTERROUND(out,  1,  6, 11, 12);
        QUARTERROUND(out,  2,  7,  8, 13);
        QUARTERROUND(out,  3,  4,  9, 14);
    }
    return;
}

int main(){
    uint32_t c[] = {0x61707865, 0x3320646e, 0x79622d32, 0x6b206574};
    return 0;
}