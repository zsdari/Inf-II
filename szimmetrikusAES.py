# #ECB tipus, legegyszerűbb, leggyengébb
# from Crypto.Cipher import AES
#
# kulcs = b"1234567890123456" #bitben tárolva
# szoveg = b"1234567890123456" #bitben tárolva
#
# cipher = AES.new(kulcs, AES.MODE_ECB) #electronic code block
# ciphertext = cipher.encrypt(szoveg) #kodolas
# print(ciphertext.hex())
#
# dekodolt_szoveg = cipher.decrypt(ciphertext) #dekodolas
# print(dekodolt_szoveg)

# #AES CBC
# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
# from Crypto.Util.Padding import pad, unpad
#
# kulcs = get_random_bytes(16)
# szoveg = 'Itt a tavasz'
# adat = szoveg.encode()
# # print(adat)
#
# iv = get_random_bytes(16)
# cipher = AES.new(kulcs, AES.MODE_CBC, iv)
# ciphertext = cipher.encrypt(pad(adat, AES.block_size))
# print(ciphertext)
#
# cipher = AES.new(kulcs, AES.MODE_CBC, iv)
# dekodolt_szoveg = unpad(cipher.decrypt(ciphertext), AES.block_size)
#
# print(dekodolt_szoveg)

# #AES GCM
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

kulcs = get_random_bytes(16)
szoveg = 'Dagad a fasz'
adat = szoveg.encode()

#kodolas
cipher = AES.new(kulcs, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(adat)
print(ciphertext)

#dekodolas
cipher = AES.new(kulcs, AES.MODE_GCM, nonce=cipher.nonce)
deciphertext = cipher.decrypt_and_verify(ciphertext, tag)
print(deciphertext)