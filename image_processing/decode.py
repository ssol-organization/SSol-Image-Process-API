import numpy as np
import pyzbar.pyzbar as pyzbar
import imutils


def decode(image):
    qr_data = pyzbar.decode(image)
    return qr_data


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + ((b[1] - a[1]) ** 2)) ** 1 / 2


def process_image(viga, image):
    if viga[0][1] != viga[1][1]:  # verifico de a altura dos qr codes é a mesma
        angle = np.sin(distance(viga[0][0], viga[0][1]))
        image = imutils.rotate(image, -angle)
    return image


def decode_all(image):
    results = decode(image)
    results_a = []
    for r in results:
        if not 'viga inicio' in str(r[0]) and not 'viga fim' in str(r[0]):
            results_a.append(r)
    return results_a