import socket
import struct
import sys

def send_dns_req(socket, domain_name, dns_address):
    xid = 42
    flags = 0x0100
    query = struct.pack('!HHHHHH', xid, flags, 1, 0, 0, 0)

    for part in domain_name.split('.'):
        query += len(part).to_bytes(1, "big")
        query += part.encode('ascii')

    query += struct.pack('!cHH', b'\x00', 1, 1)
    socket.sendto(query, (dns_address, 53))

def process_response(response_bytes):
    id, flags, qdcount, ancount, nscount, arcount = struct.unpack('!HHHHHH', response_bytes[:12])
    print("Response ID: " + str(id))
    response_code = flags & 0x0F
    if response_code != 0:
        print("Response code is " + str(response_code))
        return

    question_section = response_bytes[12:]
    question_section_ptr = 0

    while question_section[question_section_ptr] != 0x00:
        part_len = int.from_bytes(question_section[question_section_ptr:question_section_ptr+1], 'big')
        question_section_ptr += (part_len + 1)

    question_section_ptr += 2 + 2 + 1 # 1 for step from '0' and 2 + 2 for qtype and qclass

    response_section = question_section[question_section_ptr:]
    print(response_section)
    response_section_ptr = 0
    response_name_parts = []

    while response_section[response_section_ptr] != 0:
        part_len = int.from_bytes(response_section[response_section_ptr:response_section_ptr+1], 'big')
        print(part_len)
        actual_part = response_section[response_section_ptr+1:response_section_ptr+1+part_len].decode('ascii')
        response_name_parts.append(actual_part)
        print(actual_part)
        response_section_ptr += part_len + 1

    response_section_ptr += 1 # to step from '0'




if __name__ == "__main__":
    domain = sys.argv[1]
    dns_address = '8.8.8.8'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    send_dns_req(s, domain, dns_address)

    resp_bytes, sender = s.recvfrom(4093)
    process_response(resp_bytes)