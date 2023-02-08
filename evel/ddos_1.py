import time

import scapy

target_ip = "10.1.10.1"
packet_count = 1000

for i in range(packet_count):
    packet = scapy.IP(dst=target_ip)/scapy.TCP(dport=80)
    scapy.send(packet)
    time.sleep(0.1)