import time
import random

a1_timeout = 'timeouts'
prosent_i = 0

print("Starting Hack....")
time.sleep(5)
while prosent_i <= 100:
    print("Hacking FBI:", prosent_i, '%')
    time.sleep(1)
    prosent_i += random.uniform(0, 0.3)

time.sleep(5)
print(a1_timeout)
time.sleep(1)

print("FBI Hacked successfully")

