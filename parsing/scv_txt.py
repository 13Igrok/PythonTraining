import csv

# Extract data from the CSV file
data = []
with open('data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        data.append(row[0]) # adjust index as per your requirements

# Search for matching data in the text file
results = []
with open('data.txt', 'r') as file:
    for line in file:
        for item in data:
            if item in line:
                results.append(line)

# Print the results
for result in results:
    print(result)