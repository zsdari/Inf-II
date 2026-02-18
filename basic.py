import time
import math


def is_prime(number: int) -> bool:
    if not isinstance(number, int):
        return None
    if number < 2:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    for divider in range(3, int(math.sqrt(number)) + 1, 2):
        if number % divider == 0:
            return False
    return True


print("modul")

if __name__ == "__main__":
    print("main")

result = 1234 // 123

print("Result", type(result), result, end="\n")
print("izé")
prompt = "Steps:"
print(prompt)

for i in range(10):
    print("\r", end="")
    print(i, end="")
    # time.sleep(1)
print("")
print(type(prompt), prompt)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(type(numbers), numbers)

numbers.append(87)
print(type(numbers), numbers)

items = {'a': 1, 'b': 2, 'c': 3}
print(type(items), items)

elements = {'asd', 1, 1.3}
print(type(elements), elements)

print(is_prime(2))
print(is_prime("asd"))
print(is_prime(23))
print(is_prime(100))