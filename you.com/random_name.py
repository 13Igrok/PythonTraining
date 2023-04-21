import random

# Open the text file for reading
with open ( "name.txt", "r" ) as file:
    # Read the file and split it into words
    words = file.read ().split ()

    # Choose 5 random words from the list of words
    random_words = random.sample ( words, k=5 )

    # Print the random words to the console
    print ( random_words )
