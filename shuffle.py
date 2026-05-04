import random, string

str1 = '' + string.ascii_letters + string.punctuation + string.digits
str1 = list(str1)

key = str1.copy()
random.shuffle(key)

unencrypted_str = str(input("Mi a titkositando szoveg?:"))
encrypted_str = ''

for i in unencrypted_str:
    index = str1.index(i)
    encrypted_str += key[index]

print(encrypted_str)

decrypted_str = ''
for i in encrypted_str:
    index = key.index(i)
    decrypted_str += str1[index]

print(decrypted_str)
