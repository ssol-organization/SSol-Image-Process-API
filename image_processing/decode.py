import pyzbar.pyzbar as pyzbar
def decode(image):

    triangulares = []
    pontuais = []
    distribuidas = []
    apoios1 = []
    apoios2 = []

    h, w = image.shape[:2]
    image = image[:, :, ::-1]
    s = int(w / 320)
    i = 0
    j = 1
    last_size = 0
    all_data = []
    while (j < w): #divide a imagem em vários pedaços para facilitar a detecção dos qr codes
        data = pyzbar.decode(image[:, i:j])
        if data != []:
            all_data.append(data)
        if len(all_data) > last_size:
            i = j
            last_size = len(all_data)
        j += s

    for qr in all_data:
        a = str(qr[0]).replace("b\'", '').replace("\'", '').split(', ')
        if 'apoio1' in a[0]:
            apoios1.append(a)
        elif 'apoio2' in a[0]:
            apoios2.append(a)
        elif 'triangular' in a[0]:
            triangulares.append(a)
        elif 'distribuida' in a[0]:
            distribuidas.append(a)
        elif 'pontual' in a[0]:
            pontuais.append(a)

    return apoios1, apoios2, pontuais, distribuidas, triangulares