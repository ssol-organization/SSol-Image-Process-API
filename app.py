from flask import Flask, jsonify, send_file, request

import cv2
import numpy as np
import matplotlib.pyplot as plt
import io

from image_processing.detect import *
from image_processing.classify import *
from image_processing.interpret import *

app = Flask(__name__)



@app.route('/receive', methods=['GET','POST'])
def receive_image():
  
  #Retorna erro caso o parametro "foto" não seja recebido ou seja recebido vazio
  if not 'foto' in request.files or not request.files.get('foto'):
    return jsonify({'erro':'nenhum arquivo'}),400

  #Imagem recebida, na variavel "file"
  file = request.files.get('foto')

  #Imagem salva em variável estática "img"
  img = io.BytesIO()
  file.save(img)
  img.seek(0)

  #Imagem retornada, para fins de teste. Pode retornar simplesmente "sucesso" quando o código for finalizado
  return send_file(img,mimetype='image/png')


@app.route('/', methods=['GET'])

def get_info():
    try:
        #a leitura da imagem deve ser substituída pela imagem que será enviada como parâmetro
        image = cv2.imread('img/triangular_10.png')
        h, w = image.shape[:2]

        pos_viga = detect_viga(image)
        # plt.imshow(image)

        ranges = detect_viga_colors(image, pos_viga[0], pos_viga[1], pos_viga[2], pos_viga[3])

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
