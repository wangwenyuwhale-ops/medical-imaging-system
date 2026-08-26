# app/models/database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    
    patient_id = db.Column(db.String(50), primary_key=True)
    patient_name = db.Column(db.String(100))
    birth_date = db.Column(db.String(20))
    sex = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    studies = db.relationship('Study', backref='patient', lazy=True)

class Study(db.Model):
    __tablename__ = 'studies'
    
    study_uid = db.Column(db.String(100), primary_key=True)
    patient_id = db.Column(db.String(50), db.ForeignKey('patients.patient_id'), nullable=False)
    modality = db.Column(db.String(20))
    study_date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)