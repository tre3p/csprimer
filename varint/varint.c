#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MSB_MASK 0x80
#define LOW_ORDER_7_BITS_MASK 0x7F
#define VARINT_MAX_SIZE_BYTES 10
#define UINT64_T_MAX_SIZE_BYTES 8

typedef unsigned char varint;

varint *encode(uint64_t);
uint64_t decode(varint*);
void print_bytes(unsigned char*, size_t);
void print_varint(varint*);
void print_uint(uint64_t);

int main() {
    varint *encoded = encode(150);
    print_varint(encoded);
    uint64_t decoded = decode(encoded);
    printf("%d\n", decoded);

    free(encoded);
}

void print_varint(varint* varint) {
    print_bytes((unsigned char *) varint, VARINT_MAX_SIZE_BYTES);
}

void print_uint(uint64_t uint) {
    print_bytes((unsigned char *) &uint, 8);
}

void print_bytes(unsigned char* in, size_t size) {
    varint *ptr = in;

    for (int i = 0; i < size; i++) {
        printf("%.2x ", *ptr);
        ptr++;
    }
    printf("\n");
}

varint *encode(uint64_t val) {
    varint *encoded_varint = malloc(VARINT_MAX_SIZE_BYTES);
    int i = 0;

    while (i < VARINT_MAX_SIZE_BYTES && val > 0) {
        unsigned char part = val & LOW_ORDER_7_BITS_MASK;
        val >>= 7;

        if (val != 0) { // If original int != 0 - we need to set continuation bit
            part |= MSB_MASK;
        }

        encoded_varint[i] = part;
        i++;
    }

    varint *new_buff = malloc(i);
    memcpy(new_buff, encoded_varint, i);

    free(encoded_varint);

    return new_buff;
}

uint64_t decode(varint *encoded) {
    unsigned char *buff = malloc(UINT64_T_MAX_SIZE_BYTES);
    varint *encoded_ptr = encoded;

    int i = 0;
    int should_continue = 1;

    while (i < UINT64_T_MAX_SIZE_BYTES && should_continue) {
        unsigned char payload = *encoded_ptr & LOW_ORDER_7_BITS_MASK;
        print_bytes(&payload, 1);
        should_continue = *encoded_ptr & MSB_MASK; // check for continuation bit. if it's not set - we should stop loop

        buff[i] = payload;
        encoded_ptr++;
        i++;
    }

    print_bytes((unsigned char *) buff, UINT64_T_MAX_SIZE_BYTES);
    unsigned char *new_buff = malloc(i);
    memcpy(new_buff, buff, i);

    uint64_t result = *(uint64_t*) new_buff;
    free(buff);
    free(new_buff);

    return result;
}