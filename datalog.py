from mongo_setup import db

from flask import Blueprint, render_template

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
