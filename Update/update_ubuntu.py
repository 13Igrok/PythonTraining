import os

sapt = ("sudo apt-get ")
fy = (" -f -y")
up = ("update")
upg = ("upgrade")
lint = ("install")
au = ("auto")
re = ("remove")
ce = ("clear")


def update_ubuntu() -> object:
    os.system(sapt + up)
    os.system(sapt + upg + fy)
    os.system(sapt + lint + fy)
    os.system(sapt + au + re + fy)
    os.system(sapt + au + ce + fy)


update_ubuntu()
