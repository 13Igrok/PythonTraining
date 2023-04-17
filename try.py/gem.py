def gem(num):
    for i in range ( num ):
        yield i


out = gem ( 100 )
print ( type ( out ) )
for i in out:
    print ( i, end=" " )
