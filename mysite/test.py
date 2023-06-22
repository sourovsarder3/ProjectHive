print("Test.py")

r = None


def mul():
    a = 3
    b = 5
    global r
    r = a*b


mul()
print(r)
