import struct


def conceal(str):
    string_bytes = bytes(str, 'utf-8')

    if len(string_bytes) > 6:
        raise Exception("String can not be longer then 6 bytes")

    nan_double_bytes = bytes([0b01111111, 0b11111000])
    combined_bytes = nan_double_bytes + string_bytes
    return struct.unpack('>d', combined_bytes)[0]


def extract(encoded):
    double_bytes = struct.pack('>d', encoded)
    return double_bytes[2:].decode('utf-8')


enc = conceal("hello!")
print(enc)
print(extract(enc))
