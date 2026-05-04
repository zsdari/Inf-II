import string
abc = string.ascii_uppercase
# másik megoldás: chr((ord(betuk) - 65 + eltolas) % 26 + 65)

str1 = str(input("Adj meg egy szöveget: "))
push_num = int(input("Mennyi legyen az eltolás értéke eltolás: "))
str1 = str1.upper()
encrypted_str = ''

for i in range(len(str1)):
    chars = str1[i]
    chr_place = abc.find(chars)
    uj_hely = (chr_place + push_num) % 26
    encrypted_str = encrypted_str + abc[uj_hely]

print('Titkosított szöveg: ', encrypted_str)