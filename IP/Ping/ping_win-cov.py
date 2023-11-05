import csv
import io
import os
import sys

with open('websites.txt', 'r', encoding="ASCII") as file:
    reader = csv.reader(file)
    sys.stdout = io.TextIOWrapper ( sys.stdout.buffer, encoding='ASCII' )
    for row in reader:
        website = row[0]
        response = os.system("ping -c 4 " + website)
        if response == 0:
            print(website, 'is up!')
        else:
            print(website, 'is down!')
