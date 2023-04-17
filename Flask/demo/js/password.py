import random
from string import ascii_letters, digits

symbols = ascii_letters + digits
secure_rendom = random.SystemRandom ()
password = "".join ( secure_rendom.choice ( symbols ) for _ in range ( 20 ) )
print ( password )
