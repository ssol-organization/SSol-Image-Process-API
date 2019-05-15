from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_info():
    
    #codigos de visão computacional
    
    #exemplos de informações geradas
    genApoio1 = 0;
    genApoio2 = 2;
    carga1 = 20;
    posicaoApoio1=4;
    
    #retorna, em json, as informações adquiridas
    return jsonify({"genApoio1": genApoio1, "genApoio2":genApoio2,"carga1":carga1,"posicaoApoio1":posicaoApoio1})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
