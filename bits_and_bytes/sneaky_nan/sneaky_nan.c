#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define MAX_MSG_BYTES_LEN 6

double *conceal(char*);
char *extract(double*);

int main() {
    char *msg_text = "㢉㢉";
    double *encoded = conceal(msg_text);
    char *msg = extract(encoded);

    assert(strcmp(msg_text, msg) == 0);

    free(encoded);
    free(msg);
}

char *extract(double* encoded) {
    if (!encoded) return NULL;

    unsigned char *msg_bytes = (unsigned char *) encoded;
    size_t message_length = msg_bytes[1] & 0x07; // extract last 3 bits from second byte, message length stored there

    char *msg = malloc(message_length + 1); // + 1 for null terminator
    memcpy(msg, &msg_bytes[2], message_length);
    msg[message_length + 1] = '\0';

    return msg;
}

double *conceal(char *msg) {
    size_t msg_len = strlen(msg);
    if (msg_len > MAX_MSG_BYTES_LEN) {
        printf("Message length cannot be longer then 6 bytes.\n");
        return NULL;
    }

    double *nan_double = malloc(sizeof(double));
    unsigned char *nan_bytes = (unsigned char *)nan_double;

    // Set first two bytes in order to match IEEE 754 spec for NaN
    nan_bytes[0] = 0x7F; // 0b01111111
    nan_bytes[1] = 0xF8 | msg_len; // 0b11111000 | msg len. encode message length in last 3 bits

    // Set all other bytes to 0
    memset(&nan_bytes[2], 0, 6);

    // Copy message bytes
    memcpy(&nan_bytes[2], msg, msg_len);

    return nan_double;
}