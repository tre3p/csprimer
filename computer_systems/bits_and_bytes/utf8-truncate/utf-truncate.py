import sys
import struct

def safely_truncate(n, line):
    if n >= len(line):
        return line

    while n > 0 and line[n] & 0xc0 == 0x80:
        n -= 1

    return line[:n]

with open("cases", "rb") as f:
    for line in f.readlines():
        n = struct.unpack(">I", bytes([0x00, 0x00, 0x00, line[0]]))[0]
        sys.stdout.buffer.write(safely_truncate(n, line[1:-1]) + b'\n')