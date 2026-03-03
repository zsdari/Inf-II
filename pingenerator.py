"""
Write pin code generator.
4 char. Char is 0-9. (string)
Write pin code validator.
"""

import random
import string

"""
def random_generator():
    new_pin = ''
    for i in range(4):
        new_pin += str(random.randint(0, 9))
    return new_pin

print(random_generator())
"""


def get_all_pincode (n=4):
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    #state = {0: '0',1: '1',2: '2',3: '3',4: '4',5: '5',6: '6',7: '7',8: '8',9: '9'}
    pins = []
    for char0 in chars:
        for char1 in chars:
            for char2 in chars:
                for char3 in chars:
                    pins.append(char0 + char1 + char2 + char3)
    return pins

if __name__ == '__main__':
    pin_codes = get_all_pincode()
    print(pin_codes)