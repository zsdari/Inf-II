# #egyszeru elvek alapjan, kodol, dekodol, cső
#
# import random
# import string
#
# szoveg = '' + string.ascii_letters + string.digits + string.punctuation
# szoveg = list(szoveg)
#
# kulcs = szoveg.copy()
# random.shuffle(kulcs)
#
# beadott_szoveg = input("titkositando: ")
# kodolt_szoveg = ''
#
# for i in beadott_szoveg:
#     index = szoveg.index(i)
#     kodolt_szoveg += kulcs[index]
#
# #dekódolás
# dekodolt_szoveg = ''
# for i in kodolt_szoveg:
#     index = kulcs.index(i)
#     dekodolt_szoveg += szoveg[index]
#
# print(dekodolt_szoveg)
# print(kodolt_szoveg)
import string

# #ceaser kód

abc = '' + string.ascii_letters
eltolas = int(input("Eltolas merteke: (szam)"))

beadott_szoveg = input("Adja meg mit szeretne dekodolni: ")
szoveg_hossza = len(beadott_szoveg)
titkositott_szoveg = ''


for i in range(szoveg_hossza):
    betuk = beadott_szoveg[i]
    betuk_helye = abc.find(betuk)
    uj_hely = (betuk_helye + eltolas) % 26
    titkositott_szoveg += abc[uj_hely]

print(titkositott_szoveg)