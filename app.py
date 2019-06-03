from flask import Flask, jsonify

import cv2
import numpy as np
import matplotlib.pyplot as plt

from image_processing.detect import *

app = Flask(__name__)

@app.route('/', methods=['GET'])

def get_info():
    try:
        #a leitura da imagem deve ser substituída pela imagem que será enviada como parâmetro
        image = cv2.imread('img/viga_com_pesos_1000px.png')[:,:,::-1]
        h, w = image.shape[:2]

        pos_viga = detect_viga(image)


        colors_viga = detect_viga_colors(image, pos_viga[0], pos_viga[1], pos_viga[2], pos_viga[3])

        ranges = []
        for key in colors_viga:
            ranges.append(key)

        qr_data = detect_qr_codes(image, ranges)

        
        return jsonify(ImageSize = [w, h], VigaPosition = pos_viga, ColorsRGB = colors_viga, QRCodes = qr_data)
    except:
        return "Erro ao extrair informações da viga."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
