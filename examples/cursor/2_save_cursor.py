from ultra_cli import cursor



with cursor.move_temporary():
    cursor.down(3)
    print("hello")

print("bye")
