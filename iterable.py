iterable=[4,3,2,1]
for index in range(len(iterable)-1):
    iterable.insert(0, iterable[index])
print(iterable)