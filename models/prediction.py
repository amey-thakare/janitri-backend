from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(db.String(50))
    device_id = db.Column(db.String(50))

    sdp = db.Column(db.Float)

    status = db.Column(
        db.String(20)
    )

    waveform = db.Column(
        db.Text
    )

    timestamp = db.Column(
        db.String(50)
    )