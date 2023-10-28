import subprocess

hostname: str = input("IP: ")
output = subprocess.Popen(["ping", hostname], stdout=subprocess.PIPE).communicate()[0]

print(output)

if 'unreachable' not in output:
    pass
else:
    print("Offline")
