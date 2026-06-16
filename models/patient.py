from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(
        db.String(50),
        primary_key=True
    )

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gestational_week = db.Column(db.Integer)