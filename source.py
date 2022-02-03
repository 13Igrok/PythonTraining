source=[int(str(i)[::-1])for i in range(10, 18, 2)]
print(
    sorted(source, reverse=not(None))
)