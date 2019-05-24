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
        image = cv2.imread('img/viga400px.jpg')
        h, w = image.shape[:2]

        img = image
        pos_viga = detect_viga(img)

        img2 = img[:,:,::-1]
        colors_viga = detect_viga_colors(img2, pos_viga[0], pos_viga[1], pos_viga[2], pos_viga[3])

        qr_img = cv2.imread("img/4.png")
        qr_data = detect_qr_codes(qr_img)

        
        return jsonify(ImageSize = [w, h], VigaPosition = pos_viga, ColorsRGB = colors_viga, QRCodes = qr_data)
    except:
        return "Erro ao extrair informações da viga."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
