import sys

def main(we, fe, g, k, j, e):
    # wenn Ferien -> alle Gutscheine löschen
    if fe: g = 0
    # solange

if __name__ == '__main__':
    if len(sys.argv) == 7:
        we = sys.argv[1].lower() == 't'
        fe = sys.argv[2].lower() == 't'
        e = int(sys.argv[3])
        j = int(sys.argv[4])
        k = int(sys.argv[5])
        g = int(sys.argv[6])
    else:
        we = input("Wochenende (True|False):\n> ").lower() == 't'
        fe = input("Ferien (True|False):\n> ").lower() == 't'
        e = int(input("Erwachsene:\n> "))
        j = int(input("Jugentliche:\n> "))
        k = int(input("Kinder:\n> "))
        g = int(input("Gutscheine:\n> "))

    print(we, fe, e, j, k, g)
    lst = main(we, fe, g, k, j, e)

    print("Bester Preis\n", lst)
