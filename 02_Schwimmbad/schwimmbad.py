def calculate_price(we, fe, g, k, j, e):
    preise = {
              "e":  3.5,    # Erwachsener   (Einzelkarte)
              "j":  2.5,    # Jugendlischer (Einzelkarte)
              "t": 11.0,    # Tageskarte
              "f":  8.0     # Familienkarte
              }

    # Wenn Ferien -> Gutscheine ungültig
    if fe:
        g = 0

    # Am Wochenende werden keine Tageskarten verkauft
    if we:
        preise.pop("t")

    # An Wochentagen gibt es -20% Rabatt auf Einzelkarten
    else:
        preise["e"] = 2.8
        preise["j"] = 2.0

    # Wenn Kinder unter vier Jahren dabei sind
    if k > 0:
        # Wenn kein Erwachsener dabei ist -> Abbruch
        if e == 0:
            print("Kinder unter 4 Jahren müssen vin mind. einem Erwachsenen begleitet werden!")
            return False
        else:
            k = 0

    print(g, (j, e), preise)

    p_e = {e*preise['e'] + j*preise['j']: [(e, 'e'), (j, 'j')]}
    print(p_e)

    # Maximiere Anzahl an Tageskarten
    if 't' in preise:
        t_p = [e, j]
        nr_t = (e + j) // 6
        nr = nr_t * 6

        while nr > 0:
            if t_p[0] > 0:
                t_p[0] -= 1
            elif t_p[1] > 0:
                t_p[1] -= 1
            nr -= 1

        p_t = {nr_t*preise['t'] + t_p[0]*preise['e'] + t_p[1]*preise['j']: [(nr_t, 't'), (t_p[0], 'e'), (t_p[1], 'j')]}
        print(p_t)

    # Maximiere Anzahl an Familienkarten
    t_p = [e, j]
    nr_f = 0
 

if __name__ == '__main__':
    calculate_price(we=False, fe=True, g=0, k=1, j=4, e=5)
