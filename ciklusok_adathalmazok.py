"""
x = 0
while x <= 10:
    print(x)
    x += 1
    
y = True

while y:
    print('WÁÁÁÁÁ!!!')
    tovabb = input('Megy még tovább?: (0 vagy 1): ')
    if tovabb == '0':
        y = False
    else:
        y = True

print("FINISS!")    

x = int(input('Enter a number between 10 and 20: '))

while x < 10 or 20 < x:
    x = int(input('Enter a number between 10 and 20: '))
print('rendben')

#ugyanaz mint az előző
while not 10 <= x <= 20:
    x = int(input('Enter a number between 10 and 20: '))
print('rendben')

x = None
while x != '':
    x = (input('Enter'))

x = 1

while x < 100:
    print(x)
    if x % 13 == 0:
        break
    x += 1
print('Endlösung')

print('auto', end='\t') #tabulátorral megy tovább
print('motor') #enterrel ugrik tovább
print('Lastkraftwagen')

#3 soros, 5 oszlopos táblázat O-ákból
sor = 1
while sor <= 3:
    oszlop = 1
    while oszlop <= 5:
        print("O", end='')
        oszlop += 1
    print('')
    sor += 1

#Annyi O, ahány sor, derékszögű 3szög
darab = 1
sor = 1
while sor <= 7:
    oszlop = 1
    while oszlop <= darab:
        print("O", end='')
        oszlop += 1
    print('')
    darab += 1
    sor += 1

print("    O    ")
print("    O    ")
print("OOOOOOOOO")
print("    O    ")
print("    O    ")

print("forral:") #copilot

for i in range(5):
    if i == 2:
        print("OOOOOOOOO")
    else:
        print("    O    ")

print("Whileal:")

sor = 1
while sor <= 7:
    oszlop = 1
    while oszlop <= 7:
        if oszlop == 4 or sor == 4:
            print("+", end='')
        else:
            print("O", end='')
        oszlop += 1
    print('')
    sor += 1

#adatszerkezetek
lista = [2,5,10,15,25] #változtatható, [], sorszám hivatkozható
tuple01 = (2000, 3000) #nem változtatható, sem a sorrend, sem a számok, (), sorsz hivatkozható
set01 = {'1', '10', 'alma'} #elemek csak egyszer szerelphetnek benne, {}, nem rendezett, halmaz
hallgatok = {'nev' : 'István',
             'kor' : '20',
             'város' : 'Budapest'} #dictionary

print(lista) #kiírja []-is
print(*lista)
print(*lista, sep=', ') #* -al hagyható el a [], sep (separation) az elválasztó karakter (\t, \n, ' ', ', ', '; ', stb.)

print(tuple01[1])

#listák
evek = [1000, 2000, 3000, 4000] #nullától van indexdelve
print(f'Az evek: {evek[0]}, {evek[1]}, {evek[2]}, {evek[3]}') #intek

evek = ['1000', '2000', '3000', '4000'] #stringek
print(', '.join(evek))

print(len(evek)) #lista elemszama

print(*evek[2:]) #2 utáni összes elem, * --> csak elemek elválasztó meg [] nélkül
print(evek[-1]) #hátulról első elem

#ezek stringgel is ugyanazok

#üres lista feltöltése bevitelről
lista = []
adat = None
while adat != '':
    adat = input('Adat: ')
    if adat != '':
        lista.append(adat)

print(*lista, sep=', ')

#listák bejárása
lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

for i in lista: #valtozót miben keresse, lehet egy range(<szam>) is, range 0-tól n-1-ig fut
    print(i, end='\t') #soronként kiírja a lista elemeit
    print(lista.index(i)) #kiírja a lista elemeinek az indexét

# for ciklusok
for i in range(10):
    print(i)

lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
for i in range(len(lista)):
    print(i)

for i in range(0, 101, 10): #kezdő, vég, lépésköz
    print(i)

lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
index = 0

for i in lista:
    print(index, i) #index helyett lehet lista.index(i)
    index += 1

#ugyanezt máshogy:
lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

for z in range(len(lista)):
    print(z, lista[z])

#még máshogy
lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

for index, i in enumerate(lista):
    print(index, i)

#string kezelés forral
mondat = 'Geza kek az eg'

megszamole = 0
megszamolk = 0

for i in mondat:
    if i == 'e':
        megszamole += 1
    elif i == 'k':
        megszamolk += 1
print(megszamole, "\t", megszamolk)

mondat = 'Geza kek az eg'
if 'e' in mondat:
    print("Ven benne 'e' karakter")
else:
    print("Nincs benne 'e' karakter")

my_list = [10, 20, 30]
removed_item = my_list.pop(1)  # Removes and returns the item at index 1 (20), if empty removes the last item
print(my_list)

del my_list[0] #ez az indexelt elemet törli
print(my_list)

my_list.clear() #törli a lista tartalmát
print(my_list)


"""


