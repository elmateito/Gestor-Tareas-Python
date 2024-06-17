from flask import Flask
from app import db
import datetime

class Tareas(db.Model):
    idTarea = db.Column(db.Integer, Primary_key=True)
    nombreTarea = db.Column(db.String(200), nullable=False)
    fechaInicio = db.Column(db.Datetime, default=datetime.utcnow)
    fechaFin = db.Column(db.Datetime)
    estado = db.Column(db.String(20), default='Por definir')
    