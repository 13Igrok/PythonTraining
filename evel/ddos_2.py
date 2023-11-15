import socket

def scan_ports(host):
    open_ports = []
    for port in range(1, 1024):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

host = '127.0.0.1'  # замените на IP-адрес целевого хоста
open_ports = scan_ports(host)

if open_ports:
    print(f"Открытые порты на {host}: {open_ports}")
else:
    print(f"На {host} не обнаружено открытых портов.")
