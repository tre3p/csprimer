import random
import socket
import struct
import sys

if __name__ == "__main__":
    domain = sys.argv[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    xid = 42
    flags = 0x0100
    query = struct.pack('!HHHHHH', xid, flags, 1, 0, 0, 0)

    for part in domain.split('.'):
        query += len(part).to_bytes(1, "big")
        query += part.encode('ascii')

    query += struct.pack('!cHH', b'\x00', 1, 1)

    s.sendto(query, ('8.8.8.8', 53))

    resp_bytes, sender = s.recvfrom(4093)
    print(resp_bytes)
    print("OK")