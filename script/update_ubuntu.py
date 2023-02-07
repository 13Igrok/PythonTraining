import os

def update_ubuntu():
    os.system("sudo apt-get update")
    os.system("sudo apt-get upgrade -f -y")
    os.system("sudo apt-get install -f -y")
    os.system("sudo apt-get autoremove -f -y")
    os.system("sudo apt-get autoclean")
    
update_ubuntu()