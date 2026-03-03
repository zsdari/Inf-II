import math
import random

#Körös példa kódolás majd átalakítás OOP-re

circle_data = {
    'middle' : (2,5),
    'range' : 5
}
'''
def terulet(kor):
    return round(kor['range'] ** 2 * math.pi, 2) #VAGY: pow(kor['range'], 2) * math.pi

def kerulet(kor):
    return round(kor['range'] * 2 * math.pi, 2)

print(f'A kör területe: {terulet(circle_data)} \nA kör kerülete: {kerulet(circle_date)}')
'''

class Circle:
    def __init__(self, range, middle):
        self.range = range
        self.middle = middle

    def area(self):
        return round(self.range ** 2 * math.pi, 2)

    def perimeter(self):
        return round(self.range * 2 * math.pi, 2)

circle_data_01 = Circle(2,(2,5))
circle_data_02 = Circle(5,(3,7))

print(f'A kor1 terulete: {circle_data_01.area()} \n'
      f'A kor2 kerulete: {circle_data_01.perimeter()}')
print(f'A kor1 terulete: {circle_data_02.area()} \n'
      f'A kor2 kerulete: {circle_data_02.perimeter()}\n')

example_list_circle = []

for i in range(5):
    circle = Circle(random.randint(1,20), (random.randint(1,20),
                                           random.randint(1,20)))
    example_list_circle.append(circle)

for i in example_list_circle:
    print(f'A kor random sugara: {i.range}, a kozeppontja: {i.middle}\n'
          f'A kor terulete: {i.area()} \nA kor kerulete: {i.perimeter()}\n')




