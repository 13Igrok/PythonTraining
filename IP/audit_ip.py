import subprocess

hostname: str = input ( "IP: " )
output = subprocess.Popen ( ["ping", hostname], stdout=subprocess.PIPE ).communicate ()[0]

print ( output )

if "unreachable" in output:
    print ( "Offline" )
else:
    pass
