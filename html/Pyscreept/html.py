import getpass
import sys
from neiron import ConnectHandler

DEVICE_PARAMS = {
    "device_type": "cisco_ios",
    "ip": "127.0.0.1"
    "username": "python_hackir"
    "password": "hackir123"
    "secret": "secret"
}

with ConnectHandler(**DEVICE_PARAMS) as ssh:
    ssh.enable(display=1, logdir=None, context=5, format="html")
    