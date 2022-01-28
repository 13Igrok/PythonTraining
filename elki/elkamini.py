height = 10

stars = 1
for i in range(height):
    print((' ' * (height - i)) + ('^' * stars))
    stars += 2
print((' ' * height) + '|')
