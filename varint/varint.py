import struct

LOW_ORDER_7_BITS_MASK = 0x7F
MSB_MASK = 0x80

def encode(uint64t):
    result = []

    while uint64t > 0:
        part = LOW_ORDER_7_BITS_MASK & uint64t
        uint64t >>= 7

        if uint64t != 0:
            part |= MSB_MASK

        result.append(part)
    return bytes(result)

def decode(encoded):
    result = 0
    for b in reversed(encoded):
        result <<= 7
        result |= b & LOW_ORDER_7_BITS_MASK
    return result

encoded = encode(150)
print(encoded)
print(decode(encoded))