from lib2to3.pygram import Symbols
import random
from string import digits
from string import ascii_letters

symbols = ascii_letters + digits
secure_rendom = random.SystemRandom()
password = "".join(secure_rendom.choice(symbols)
                   for i in range(20))
print(password)
