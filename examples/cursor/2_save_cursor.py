from pymenus import cursor

# with cursor.SaveCursor():
#     cursor.down(3)
#     print("hello")

# print("bye")


import sys
def stdout(string):
    sys.stdout.write(string)
    sys.stdout.flush()

stdout('\033[2J')
