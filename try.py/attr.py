class A:
    def __init__(self):
        self.attr = 1


class B(A):
    def __init__(self):
        super().__init__()


class C(A):
    def __init__(self):
        self.attr = 2


class D(B, C):
    def __init__(self):
        super().__init__()


d = D()
print(d.attr)
