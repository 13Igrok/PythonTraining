import os
from shlex import quote as shlex_quote

sapt = ("sudo apt-get ")
fy= (" -f -y")
up=("update")
upg=("upgrade")
fin=("&&")
int=("install")
au=("auto")
re=("remove")
ce=("clear")
def update_ubuntu() -> object:
    os.system ( shlex_quote ( sapt ) + up + fin sapt + upg + fy + fin + sapt + int + fy + fin + sapt + au + re + fy + fin + sapt + au + ce + fy)
    
update_ubuntu()