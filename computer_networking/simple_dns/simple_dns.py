import socket
import struct
import sys
import random

DNS_ADDRESS = "8.8.8.8"
DNS_DEFAULT_PORT = 53

def send_dns_request(socket, dns_address, dns_port, query):
    print("Sending DNS request to " + dns_address)
    socket.sendto(query, (dns_address, dns_port))
    
def receive_dns_response(socket):
    resp_bytes, sender = socket.recvfrom(4093)
    print("Received response from " + str(sender[0]))
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
        return
        
def validate_dns_response(response_bytes, request_id):
    response_id, flags = struct.unpack("!HH", response_bytes[:4])
    if response_id != request_id:
        print("Response received with ID " + str(id) + ". However, request ID was " + str(request_id))
        return False
        
    if ((flags & 0x8000) >> 15) != 1:
        print("Received response isn't response for original request")
        return False
        
    rcode = flags &0x000F
    if rcode != 0:
        print("Received RCODE isn't 0. RCODE: " + str(rcode))
        return False
        
    return True

def dns_lookup(dns_address, domain_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    (req_id, message) = construct_dns_request(domain_name)
    send_dns_request(sock, DNS_ADDRESS, DNS_DEFAULT_PORT, message)
    resp_bytes = receive_dns_response(sock)
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