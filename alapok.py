"""

#beker = input("Adj meg egy számot: ") #ez így csak egy string
#szam = int(beker) #így már szám

#print(type(szam))

num =int(input("Szám be: "))

num = num + 0.1

print(num)

x = 10
y = 20

print("A két szám összege:", x + y)
print("A két szám különbsége:", x - y)
print("A két szám szorzata:", x * y)
print("A két szám hányadosa:", x / y)
print("A két szám egész osztásának maradéka:", x%y)

x = "Kőbánya"
y = "Kispest"

print(x+"-"+y)

x = 3
x = x + 10
x += 10
print(x)

x-= 20
print(x)

#+,-,*,/ is lehet +=, -=, *=, /=, ciklus léptetésnél lehet mindegyiket használni!

beker = int(input("Adj meg egy számot: "))
if beker < 0:
    print('negativ')
elif beker == 0: # '=' műveleti jel/matematikai egyenlőség, '==' ellenőrzés
    print('nulla')
else:
    print("pozitív")

import random

veletlensz = random.randint(-100, 100)
print(f'A generált szám: {veletlensz}') # ugyanaz, mint: print('A generált szám:', veletlensz)
if veletlensz < 0: #ez így értelmetlen mert sosem lesz null vagy positive, több külön eset kell arra hogy mindegyiket vizsgáljuk!
    print('negative')
elif veletlensz % 2 == 0:
    print('páros')
elif veletlensz % 2 == 1:
    print('páratlan')
elif veletlensz == 0:
    print('null')
elif veletlensz > 0:
    print('positive')

import random
a = random.randint(-100, 100)
b = random.randint(-100, 100)

print(f'A generált számok: {a} és {b}, milyen műveletet végezzünk velük?')
muvelet = input('Add meg a műveleti jelet: ')

match muvelet:
    case '+':
        print(f'{a} {muvelet} {b} = {a+b}')
    case '-':
        print(f'{a} {muvelet} {b} = {a-b}')
    case '*':
        print(f'{a} {muvelet} {b} = {a*b}')
    case '/' if b != 0:
        print(f'{a} {muvelet} {b} = {a/b}')
    case '**':
        print(f'{a} {muvelet} {b} = {a**b}')
    case other:
        print("Ez nem műveleti jel!")
"""

"""
    ==
    !=
    <
    <=
    >
    >=
    and
    or    
    not
"""

x = 10
y = 20

if x < 0 and y < 0:
    print('mind a kettő negativ')
if x < 0 or y < 0:
    print('van köztük negatív')
if not x <= 0:
    print('x pozitív')

