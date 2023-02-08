while True:
    expression = input("Enter expression: ")
    if expression == 'quit':
        break
    result = eval(expression)
    print("Result =", result)