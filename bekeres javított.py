import random
import sys

print("Mi legyen a ket szelsoertek?: ")
minim = int(input())
maxim = int(input())
start_num = 0


def select(label, menu):
    print(label)
    for item in menu:
        print(f'\t - {menu.index(item)}: {item}')
    result = get_int(prompt="Válassz egyet! ", max=len(menu) - 1)
    return result


def get_int(prompt="> ", min=0, max=None):
    while True:
        result = input(prompt).strip()
        if result == 'exit':
            sys.exit(0)
        # command kezelés
        try:
            value = int(result)
            if value < min:
                print(f'A szam nem lehet kisebb mint {min}!')
                continue
            if max is not None and value > max:
                print(f'A szam nem lehet nagyobb mint {max}!')
                continue
            return value
        except ValueError:
            print("A megadott értéknek számnak kell lennie!")
            continue


def start_game():
    print("Gondoltam egy szamra, talald ki!")
    num = random.randint(minim, maxim)
    remaining = 8
    while remaining > 0:
        print(f'Még {remaining} próbálkozásod van!')
        print("Tipp: ", end=" ")
        start_num = get_int(min=minim, max=maxim)
        if start_num == num:
            print("Nyertél!")
            return True
        else:
            if start_num > num:
                print("Kisebb kell neked!")
            if start_num < num:
                print("Nagyobb kell neked!")

        remaining -= 1
    print("Vesztettél!")
    return False

if __name__ == "__main__":
    print("Hello!")
    while True:
        r = select("Szeretnel-e jatszani?", ["Igen", "Nem"])
        if r == 0:  # Igen
            start_game()
        else:  # Nem
            sys.exit(0)

        result = get_int(prompt="Szeretnel meg jatszani? (0 - Igen, 1 - Nem): ", max=1)
        if result == 1:
            sys.exit(0)