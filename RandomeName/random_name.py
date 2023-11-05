import io
import random
import sys

# Open the text file for reading
with open("name.txt", "r", encoding="utf-8") as file:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # Read the file and split it into words
    words = file.read().split()

    # Choose 5 random words from the list off words
    random_words = random.sample(words, k=5)

    # Print the random words to the console
    print(f'{random_words}')