# padrão de retorno:
# [tipo, modulo, posicao_i]
# posicao i é a posição inicial do objeto, como as distancias sao constantes nao é necessário posicao f pra objetos

def classify(data, position):
    result = []
    for i in data:
        if i == []: break
        info = i.split('\\n')
        t = info[0].split('t:')[1]
        w = None if info[1].split('w:')[1] == '0' else int(info[1].split('w:')[1])
        if 'apoio' in t:
            result.append(classify_apoios(t, position))
        else:
            result.append(classify_cargas(t, w, position))
    return result


def classify_apoios(t, position):
    return [t, None, position] if t == 'apoio1' else [t, None, position]


def classify_cargas(t, w, position):
    return [t, w, position]