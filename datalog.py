from mongo_setup import db

from flask import Blueprint, render_template, request, jsonify, make_response, Response
from datetime import datetime
import pytz
import io
import csv
import zipfile

datalog = Blueprint('datalog', __name__)


class DataLog:
    def __init__(self, uploadedData, timePlayed, status):
        self.uploadedData = uploadedData
        self.timePlayed = timePlayed
        self.status = status

    def save(self):
        collection = db['datalogs']  # Nome da coleção
        data = {
            'uploadedData': self.uploadedData,
            'timePlayed': self.timePlayed,
            'status': self.status
        }
        result = collection.insert_one(data)
        return result.inserted_id

    @staticmethod
    def find_all():
        collection = db['datalogs']
        logs = collection.find()
        return [DataLog(**log) for log in logs]

    def __str__(self):
        return f"{self.uploadedData} - {self.timePlayed} - {self.status}"


@datalog.route('/datalogs/upload', methods=['POST'])
def formulario():
    brasil_timezone = pytz.timezone('America/Sao_Paulo')
    # data_atual_brasil = datetime.now(brasil_timezone)

    # Obtenha a data e hora atual
    data_hora_atual = datetime.now()

    # Formate a data e hora no formato desejado
    data_hora_formatada = data_hora_atual.strftime("%Y-%m-%dT%H:%M:%SZ")

    time_played_str = request.form.get('timePlayed')

    # Use strptime para analisar a string e criar um objeto datetime
    time_played_datetime = datetime.strptime(time_played_str, "%Y-%m-%dT%H:%M:%SZ")

    uploadedData = datetime.strptime(data_hora_formatada, "%Y-%m-%dT%H:%M:%SZ")
    timePlayed = time_played_datetime
    status = request.form.get('status')

    # Crie uma instância da classe DataLog e salve no banco de dados
    log = DataLog(uploadedData, timePlayed, status)
    log.save()

    return '', 200
@datalog.route('/datalogs', methods=['GET'])
def get_all_data():
    docs = get_all_documents()

    for log in docs:
        log['_id'] = str(log['_id'])

        log['timePlayed'] = log['timePlayed'].strftime("%Y-%m-%dT%H:%M:%SZ")
        log['uploadedData'] = log['uploadedData'].strftime("%Y-%m-%dT%H:%M:%SZ")

    return jsonify(docs)

@datalog.route('/datalogs/latest-uploaded-total', methods=['GET'])
def get_latest_uploaded_data():
    # Acessar a coleção que contém os registros de DataLog
    collection = db['datalogs']

    # Encontrar o registro mais recente ordenando por 'uploadedData' em ordem decrescente
    mais_recente = collection.find_one(sort=[('uploadedData', -1)])

    if mais_recente is None:
        return make_response(jsonify({"error": "Nenhum dado encontrado"}), 404)

    # Acessar o campo 'uploadedData' no documento mais recente
    data_mais_recente = mais_recente['uploadedData']

    return jsonify({"latestUploadedData": data_mais_recente.isoformat()})

@datalog.route('/datalogs/status/count', methods=['GET'])
def perform_aggregation():
    # Acessar a coleção que contém os documentos a serem agregados
    collection = db['datalogs']

    # Pipeline de agregação
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
        {"$project": {"status": "$_id", "_id": 0, "count": 1}}
    ]

    # Executar a operação de agregação
    aggregation_result = list(collection.aggregate(pipeline))

    return jsonify(aggregation_result)


def get_all_documents():
    collection = db['datalogs']
    return list(collection.find())


# Método para gerar um arquivo CSV a partir dos documentos
def generate_csv(documentos):
    output = io.StringIO()
    writer = csv.writer(output)

    # Escrever cabeçalho do CSV (use as chaves do primeiro documento como cabeçalho)
    if documentos:
        header = documentos[0].keys()
        writer.writerow(header)

    for doc in documentos:
        writer.writerow(doc.values())

    output.seek(0)
    return output


@datalog.route('/datalogs/downloaddata', methods=['GET'])
def download_csv_zip():
    # Obter todos os documentos da coleção
    documents = get_all_documents()

    # Gerar um arquivo CSV a partir dos documentos
    csv_data = generate_csv(documents)

    # Criar um arquivo ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('dados.csv', csv_data.getvalue())

    # Configurar a resposta HTTP
    response = Response(zip_buffer.getvalue())
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = 'attachment; filename=dados.zip'

    return response


