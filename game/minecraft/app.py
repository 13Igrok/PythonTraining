import subprocess

subprocess.call(["java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"])