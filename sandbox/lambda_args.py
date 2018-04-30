def show(x):
    print x

def callit(color):
    f = lambda: show(color)
    f()

callit('red')
callit('blue')