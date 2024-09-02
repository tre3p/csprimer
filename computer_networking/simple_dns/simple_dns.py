import socket
import struct
import sys
import random
import time

DNS_ADDRESS = "8.8.8.8"
DNS_DEFAULT_PORT = 53

class QuestionSection:
    def __init__(self, qname, qtype, qclass):
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

def send_dns_request(socket, dns_address, dns_port, query):
    print("Sending DNS request to " + dns_address)
    socket.sendto(query, (dns_address, dns_port))
    return time.time()
    
def receive_dns_response(socket, sent_request_time):
    resp_bytes, sender = socket.recvfrom(4093)
    received_response_time = time.time()
    delta = (received_response_time - sent_request_time) * 1000
    print("Received response from " + str(sender[0]) + " in " + str(round(delta, 2)) + " ms")
    return resp_bytes
    
def construct_dns_request(domain_name):
    id = random.randint(0, 65535)
    qdcount = 1
    
    flags = 0x00
    flags |= 0x0100 # recursion query desired
    
    message = struct.pack('!HHHHHH', id, flags, qdcount, 0, 0, 0)
    
    for part in domain_name.split('.'):
        message += len(part).to_bytes(1, 'big')
        message += part.encode('ascii')
    
    message += b'\x00' # terminate hostname
    
    qtype = 1
    qclass = 1
    
    message += struct.pack("!HH", qtype, qclass)
    
    return (id, message)
    
def process_dns_response(response_bytes):
    question_section = response_bytes[12:] # 12 bytes to skip header section
    question, question_end_ptr = parse_question_section(question_section)
    
    answer_section = question_section[question_end_ptr:]
    decoded_hostname, qname_end_ptr = parse_answer_section(answer_section)
    #print(decoded_hostname)
    
    #type, rdata_class, ttl, rdlength = struct.unpack('!HHIH', response_bytes[qname_end_ptr:qname_end_ptr+10])
    #print(rdlength)
    #print(response_bytes[qname_end_ptr+10:])
    
def parse_answer_section(response_bytes):
    name, name_end_ptr = decode_name(response_bytes)
    return (name, 1)
    
def parse_question_section(question_section):
    qname, qname_end_ptr = decode_name(question_section)
    qtype, qclass = struct.unpack('!HH', question_section[qname_end_ptr:qname_end_ptr+4])
    qname_end_ptr += 4 # + 2 for qtype and +2 for qclass
    
    return QuestionSection(qname, qtype, qclass), qname_end_ptr

def decode_name(response_bytes):
    name_ptr = 0
    name_parts = []
    
    while True:
        b_len = int.from_bytes(response_bytes[name_ptr:name_ptr+1], 'big')
        if b_len == 0:
            name_ptr += 1 # advance ptr by one byte to point to the start of the next section
            break
            
        name_ptr += 1 # add one byte because of read length octet
        part = response_bytes[name_ptr:name_ptr+b_len]
        name_ptr += b_len # advance pointer by len of extracted host part
        name_parts.append(part.decode('ascii'))
        
    decoded_host = '.'.join(name_parts)
    return (decoded_host, name_ptr)
        
        
def validate_dns_response(response_bytes, request_id):
    response_id, flags = struct.unpack("!HH", response_bytes[:4])
    if response_id != request_id:
        print("Response received with ID " + str(id) + ". However, request ID was " + str(request_id))
        return False
        
    if ((flags & 0x8000) >> 15) != 1:
        print("Received response isn't response for original request")
        return False
        
    rcode = flags & 0x000F
    if rcode != 0:
        print("Received RCODE isn't 0. RCODE: " + str(rcode))
        return False
        
    return True

def dns_lookup(dns_address, domain_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    (req_id, message) = construct_dns_request(domain_name)
    sent_time = send_dns_request(sock, DNS_ADDRESS, DNS_DEFAULT_PORT, message)
    resp_bytes = receive_dns_response(sock, sent_time)
    if validate_dns_response(resp_bytes, req_id):
        process_dns_response(resp_bytes)
    else:
        print("Received response isn't valid, aborting DNS lookup..")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: simple_dns *domain*")
    else:
        domain = sys.argv[1]
        dns_lookup(DNS_ADDRESS, domain)