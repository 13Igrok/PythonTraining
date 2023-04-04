import os
from shlex import quote as shlex_quote

sapt = ("sudo apt-get ")
fy= (" -f -y")
up=("update")
upg=("upgrade")
int=("install")
au=("auto")
re=("remove")
ce=("clear")
def update_ubuntu() -> object:
    os.system(sapt+up)
    os.system(sapt+upg+fy)
    os.system(sapt+int+fy)
    os.system(sapt+au+re+fy)
    os.system(sapt+au+ce+fy)
    
update_ubuntu()
