def f(x: int):
    def g(y: int):
        print(2)
    y: int = 3
    print(1)
    g(x)

