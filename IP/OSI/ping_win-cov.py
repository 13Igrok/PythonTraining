import os

with open ("../../ip_list.txt") as file:
    park = file.read().splitlines()
    output = ""
    for ip in park:
        response = os.popen(f"ping -c 4 -n {ip} ").read()
        if ("Request timed out." in response or "unreachable" in response):
            output += str(ip) + ' link is down'+'\n'
        else:
            output += str(ip) + ' is up '+'\n'
    with open("ip_output.txt", "w") as file:
        file.write(output)
