import socket
from contextlib import closing


def is_port_open(ip, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        return sock.connect_ex((ip, port)) == 0


def scan_ports(ip, port_range):
    open_ports = []
    for port in port_range:
        if is_port_open(ip, port):
            open_ports.append(port)
    return open_ports


ip = '10.1.10.1'  # replace with your IP address
port_range = range(1, 65500)  # replace with your desired port range

open_ports = scan_ports(ip, port_range)
print(f"Open ports on {ip}: {open_ports}")
