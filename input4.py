n=int(input("Число : "))
for i in range(-n+1,n):
    if((n-abs(i))%2)==1:
        print(n-abs(i),end=" ")
    else:
        print("@ ",end=" ")