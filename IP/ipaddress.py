import ipaddress
Adr = input("Enter: ")
net = ipaddress.ip_network('Adr')
for addr in net:
    print(addr)
