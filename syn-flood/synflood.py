import struct
import datetime
from typing import List

PCAP_HEADER_SIZE_BYTES = 4 + 2 + 2 + 4 + 4 + 4 + 4
PCAP_MAGIC_NUMBER = 0xa1b2c3d4
PCAP_MAJOR_VERSION_NUMBER = 2
PCAP_MINOR_VERSION_NUMBER = 4
TCP_SYN_ACK_FLAG_MASK = 0x12

class CapturedPacket:
    def __init__(self, capture_ts, packet_bytes):
        self.capture_ts = capture_ts
        self.packet_bytes = packet_bytes

def validate_pcap_header(pcap_savefile_bytes):
    magic_number = struct.unpack("<I", pcap_savefile_bytes[:4])[0]

    if magic_number != PCAP_MAGIC_NUMBER:
        raise Exception("PCAP magic number doesn't match. Actual magic number is: " + magic_number)

    major_version_number = struct.unpack("<H", pcap_savefile_bytes[4:4+2])[0]
    minor_version_number = struct.unpack("<H", pcap_savefile_bytes[6:6+2])[0]

    if major_version_number != PCAP_MAJOR_VERSION_NUMBER or minor_version_number != PCAP_MINOR_VERSION_NUMBER:
        raise Exception("PCAP versions doesn't match. Actual version is: " + f'{major_version_number}.{minor_version_number}')

def parse_pcap_per_packet_headers(pcap_savefile_bytes):
    per_packet_start_bytes = pcap_savefile_bytes[PCAP_HEADER_SIZE_BYTES:]
    packet_pointer = 0
    captured_packets = []

    while packet_pointer < len(per_packet_start_bytes):
        packet_capture_timestamp = struct.unpack("<I", per_packet_start_bytes[packet_pointer:packet_pointer+4])[0]
        ts = datetime.datetime.fromtimestamp(packet_capture_timestamp)
        packet_pointer += 4

        packet_capture_microseconds = struct.unpack("<I", per_packet_start_bytes[packet_pointer:packet_pointer+4])[0]
        packet_pointer += 4

        packet_truncated_length = struct.unpack("<I", per_packet_start_bytes[packet_pointer:packet_pointer+4])[0]
        packet_pointer += 4

        packet_untruncated_length = struct.unpack("<I", per_packet_start_bytes[packet_pointer:packet_pointer+4])[0]
        packet_pointer += 4

        captured_packets.append(CapturedPacket(ts, per_packet_start_bytes[packet_pointer:packet_pointer+packet_truncated_length]))

        packet_pointer += packet_truncated_length

    return captured_packets

def analyze_captured_packets(captured_packets: List[CapturedPacket]):
    result = {
        "server": {"syn": 0, "ack": 0, "syn-ack": 0},
        "client": {"syn": 0, "ack": 0, "syn-ack": 0},
    }

    for packet in captured_packets:
        ihl = packet.packet_bytes[4] & 0x0f
        total_header_length_bytes = 4 + ihl * 4 # times 4, because ihl specifies the number of 32-bit words. plus 4 because of ll_header

        tcp_header = packet.packet_bytes[total_header_length_bytes:]

        sender_port = struct.unpack(">I", bytes([0x00, 0x00]) + tcp_header[:2])[0] # pad with 2 bytes to interpet as big-endian int
        tcp_flags_masked = tcp_header[13] & TCP_SYN_ACK_FLAG_MASK

        sender = result["server" if sender_port == 80 else "client"]

        if tcp_flags_masked == 18:
            sender["syn-ack"] += 1
        elif tcp_flags_masked == 16:
            sender["ack"] += 1
        elif tcp_flags_masked == 2:
            sender["syn"] += 1

    return result


f = open("synflood.pcap", "rb")
pcap_file_bytes = f.read()
validate_pcap_header(pcap_file_bytes)
captured_packets = parse_pcap_per_packet_headers(pcap_file_bytes)

print("Analyzing " + str(len(captured_packets)) + " of captured packets")
analyzed_packets = analyze_captured_packets(captured_packets)

print(str(int(analyzed_packets["server"]["syn-ack"] / analyzed_packets["client"]["syn"] * 100)) + "%")