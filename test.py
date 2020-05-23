def fun():
    print('a')

x = fun
d = {1: fun}

d[1]()