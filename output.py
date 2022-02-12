input_data = [
    "foobar", ["test", 76, ()],
    {"one": 2, "two": 1}, frozenset()
]
output = list(filter(lambda x: len(x) > 3 or len(x) == 2, input_data))
print(output)
