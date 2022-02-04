def gem(num):
    for i in range(num):
        yield i


out = gem(6)
print(type(out))
for i in out:
    print(i, end=" ")
