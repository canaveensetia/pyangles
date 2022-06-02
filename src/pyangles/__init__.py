from .main import Pyangles

def go(df, key, window, order):
    t = Pyangles()
    return t.search(df, key, window, order)

