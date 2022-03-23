class Alpha:

    result = 64

    def start(self):
        while not self.func():
            self.k -= 3

    def func(self):
        if self.k != False:
            self.result //= 2
            return False
        return True


A = Alpha()
A.start()
print(A.result)
