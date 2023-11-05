import linecache
from typing import Any


def get_nums(i):
    enum: list[Any] = []
    for n in linecache:
        if n % 2 == 0:
            enum.append(n)
        if n > 90:
            break
    return enum


nums = (10, 20[25, 77, 82, 85, 90])
print(get_nums(nums[2]))
