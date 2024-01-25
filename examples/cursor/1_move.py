import time

from ultra_cli import cursor



print("1. This text will be overridden")
print("2. This text will be overridden")

cursor.up(2)

time.sleep(2)

print("this is the new content of line 1")
print("this is the new content of line 2")



cursor.forward(5)

print("hello world")
