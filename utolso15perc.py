lista = [10,20,30,40,50]
print(*lista, sep=', ')

kivalogatas = [x * 2 for x in lista] #az elemek dupláját beleteszi az új listába
print(*kivalogatas, sep=', ')

kivalogatas02 = [i * 2 for i in lista if i % 20 == 0] #azoknak az elemeknek a dupláját amelyek oszthatóak 20-al beleteszi az új listába
print(*kivalogatas02, sep=', ')


#jegyek átlagát számoljuk ki

jegyek = [1,3,4,5,2,3,4,2,1,5,5,5,1]

osszeg = 0
for i in jegyek:
    osszeg += i
print(f'A jegyek átlaga: {osszeg / len(jegyek)}')
print(f'A jegyek átlaga: {osszeg / len(jegyek):.2f}') #2 tizedesre kerekítve
