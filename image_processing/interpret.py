def interpret(all_qr_codes):
    apoio1 = []  # cada apoio terá posição inicial, final
    apoio2 = []
    triangular = []  # cada triangulo: (pos_i(x, y), pos_f(x, y), peso)
    distribuida = []
    pontual = []  # cada pontual: (pos_i(x, y), pos_f(x, y), peso)
    i = 0
    begin = []
    end = []
    peso = 0
    finish_triangulo = False
    finish_distribuida = False
    while i < len(all_qr_codes):
        if len(all_qr_codes[i]) > 0:
            if 'triang' in all_qr_codes[i][0][0]:
                finish_triangulo = not finish_triangulo
                peso = all_qr_codes[i][0][1]
                if len(all_qr_codes[i]) == 1:
                    begin = [i * 10, 10]
                else:
                    y = 0
                    if all_qr_codes[i][0][1] == 10:
                        y = 40
                    elif all_qr_codes[i][0][1] == 6:
                        y = 30
                    else:
                        y = 20
                    end = [(i + 1) * 10, y]
                if not finish_triangulo:
                    triangular.append([begin, end, peso])  # triangular = (pos_i(x, y), pos_f(x, y), peso)

            elif 'pontual' in all_qr_codes[i][0][0]:
                altura = all_qr_codes[i][0][1] * 10
                peso = all_qr_codes[i][0][1]
                pontual.append(
                    [i * 10, (i + 1) * 10, altura, peso])  # pontual = (pos_i(x, y), pos_f(x, y), peso)
                # os y são iguais por ser no máximo uma coluna

            elif 'apoio 2' in all_qr_codes[i][0][0]:  # apoio = (xi, xf)
                pos = [i * 10, (i + 1) * 10]
                apoio2.append(pos)

            elif 'apoio 1' in all_qr_codes[i][0][0]:  # apoio = (xi, xf)
                pos = [i * 10, (i + 1) * 10]
                apoio1.append(pos)
            elif 'distr' in all_qr_codes[i][0][0]:
                peso = all_qr_codes[i][0][1]
                if not finish_distribuida:
                    begin = i * 10
                    finish_distribuida = not finish_distribuida
                else:
                    end = (i + 1) * 10
                    distribuida.append([begin, end, peso])
        i += 1
    return [apoio1, apoio2, pontual, distribuida, triangular]