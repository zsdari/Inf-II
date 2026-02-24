import random

def kockadobas():
    return random.randint(1,6)

if __name__ == "__main__":
    print("A dobott szam: ", end=" ")
    print(kockadobas())

    megszamol = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0}

    for i in range (10000):
        tmp = kockadobas()
        megszamol[tmp] += 1

    print("Dobások eredménye:")
    for kulcs, ertek in megszamol.items():
        print(f"{kulcs}: {ertek} db", end = "\t")