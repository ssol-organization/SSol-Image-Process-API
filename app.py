from flask import Flask, jsonify

import cv2
import numpy as np
import matplotlib.pyplot as plt

from image_processing.detect import *
from image_processing.classify import *
from image_processing.interpret import *

app = Flask(__name__)

@app.route('/', methods=['GET'])

def get_info():
    try:
        #a leitura da imagem deve ser substituída pela imagem que será enviada como parâmetro
        image = cv2.imread('img/capture (3).jpg')
        print(image)
        h, w = image.shape[:2]

        pos_viga = detect_viga(image)
        # plt.imshow(image)

        ranges = detect_viga_colors(image, pos_viga[0], pos_viga[1], pos_viga[2], pos_viga[3])
        print(ranges)
        # plt.imshow(image)

        qr_data = detect_qr_codes(image, ranges)

        infos = []
        for t in qr_data:
            infos.append(classify(qr_data[t], t))

        pesos_apoios = interpret(infos)
        print(pesos_apoios)

        return jsonify(apoios = {"apoios_tipo1_positions":pesos_apoios[0], "apoios_tipo2_positions":pesos_apoios[1]}, cargas = {"pontuais":pesos_apoios[2], "distribuidas":pesos_apoios[3],"triangulares":pesos_apoios[4]})
    except:
        return "Erro ao extrair informações da viga."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)