from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/crearworkflow', methods=['GET'])
def crearworkflow():
    return jsonify({"resultado": "Workflow"})

'''@app.route('/funcionalidad2', methods=['POST'])
def ejecutar_funcionalidad2():
    data = request.json
    return jsonify({"resultado": f"Funcionalidad2 ejecutada con {data['parametro1']}"})'''