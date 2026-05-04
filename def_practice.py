#1. Aufgabe
import math
from unittest import case


def summary(a, b):
    return a + b

print(summary(1, 2))


#2. Aufgabe
def is_even(num):
    return num % 2 == 0
print(is_even(2))

#3.1 Aufgabe
num_list = [1, 2, 3, 4, 5,6,9,12,15,10,11,13,14]
def is_divideable_with3(num_list):
    num_of_tru = 0
    for num in num_list:
        if num % 3 == 0:
            num_of_tru += 1
    return num_of_tru
print(is_divideable_with3(num_list))

#3.2 Aufgabe
num_list = []
input_num = int(input("Enter a number: "))
while input_num >= 0:
    num_list.append(input_num)
    input_num = int(input("Enter another number: "))

def is_divideable_with3(num_list):
    num_of_tru = 0
    for num in num_list:
        if num % 3 == 0:
            num_of_tru += 1
    return num_of_tru
print(is_divideable_with3(num_list))

#4. Aufgabe
def circumference(len_of_side, *num_of_sides):
    match len(num_of_sides):
        case 0:
            return 4 * len_of_side
        case 1:
            return 2 * (len_of_side + num_of_sides[0])
        case 2:
            return len_of_side + num_of_sides[0] + num_of_sides[1]
        case 3:
            return len_of_side + sum(num_of_sides)

print(circumference(4, 5, 6))

#5. Aufgabe
num_list_2 = []
input_num = int(input("Enter a number: "))
while input_num >= 0:
    num_list_2.append(input_num)
    input_num = int(input("Enter another number: "))

def smallest_finder(num_list_2):
    #return min(num_list_2) way too easy way
    smallest_num = num_list_2[0]
    for num in num_list_2:
        if num < smallest_num:
            smallest_num = num
    return smallest_num

print(smallest_finder(num_list_2))