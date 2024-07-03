#include <assert.h>
#include <stdio.h>

int bitcount(unsigned);

int main() {
    assert(bitcount(0) == 0);
    assert(bitcount(1) == 1);
    assert(bitcount(3) == 2);
    assert(bitcount(8) == 1);
    // harder case:
    assert(bitcount(0xffffffff) == 32);
    printf("OK\n");
}

int bitcount(unsigned n) {
    int count = 0;

    while (n) {
        count += n & 0x01;
        n >>= 1;
    }

    return count;
}