from fastapi import FastAPI, HTTPException
from database import engine
from models.base import Base
from models.patient import Patient
from models.prediction import Prediction
import time
from schemas import WaveformRequest
from services.cnn_service import model
from services.cnn_service import EXPECTED_LENGTH
from pydantic import BaseModel

from database import SessionLocal
from models.prediction import Prediction

import numpy as np
import json

from models.patient import Patient

app = FastAPI(
    title="Janitri API"
)

time.sleep(10)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Janitri FastAPI Running"
    }

@app.post("/upload-waveform")
def upload_waveform(data: WaveformRequest):

    db = SessionLocal()

    try:

        signal = np.array(
            data.signal,
            dtype=np.float32
        )

        from fastapi import HTTPException

        if len(signal) != EXPECTED_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Expected {EXPECTED_LENGTH} samples"
            )

        original_signal = signal.copy()

        signal = signal / 4.0

        signal = signal.reshape(
            1,
            EXPECTED_LENGTH,
            1
        )

        prediction = model.predict(
            signal,
            verbose=0
        )

        sdp = float(
            prediction[0][0]
        )

        status = (
            "NORMAL"
            if 2 <= sdp <= 8
            else "ABNORMAL"
        )
        patient = (
        db.query(Patient)
        .filter(
        Patient.patient_id == data.patient_id
        )
            .first()
    )

        if not patient:

            patient = Patient(
            patient_id=data.patient_id,
            name="Test Patient",
            age=28,
            gestational_week=34
            )

            db.add(patient)
            db.commit()

        record = Prediction(
            patient_id=data.patient_id,
            device_id=data.device_id,
            sdp=sdp,
            status=status,
            waveform=json.dumps(
                original_signal.tolist()
            ),
            timestamp=data.timestamp
        )

        db.add(record)
        db.commit()

        return {
            "sdp": round(sdp, 2),
            "status": status
        }

    finally:
        db.close()

@app.get("/patients")
def get_patients():

    db = SessionLocal()

    try:

        patients = db.query(
            Patient
        ).all()

        return [
            {
                "patient_id": p.patient_id,
                "name": p.name,
                "age": p.age,
                "gestational_week": p.gestational_week
            }
            for p in patients
        ]

    finally:
        db.close()

@app.get("/latest/{patient_id}")
def latest_prediction(patient_id: str):

    db = SessionLocal()

    try:

        prediction = (
            db.query(Prediction)
            .filter(
                Prediction.patient_id == patient_id
            )
            .order_by(
                Prediction.id.desc()
            )
            .first()
        )

        if not prediction:
            raise HTTPException(
                status_code=404,
                detail="No prediction found"
            )

        return {
            "patient_id": prediction.patient_id,
            "device_id": prediction.device_id,
            "sdp": prediction.sdp,
            "status": prediction.status,
            "timestamp": prediction.timestamp
        }

    finally:
        db.close()

@app.get("/history/{patient_id}")
def history(patient_id: str):

    db = SessionLocal()

    try:

        predictions = (
            db.query(Prediction)
            .filter(
                Prediction.patient_id == patient_id
            )
            .order_by(
                Prediction.id.desc()
            )
            .limit(20)
            .all()
        )

        return [
            {
                "sdp": p.sdp,
                "status": p.status,
                "timestamp": p.timestamp
            }
            for p in predictions
        ]

    finally:
        db.close()

@app.get("/waveform/{patient_id}")
def waveform(patient_id: str):

    db = SessionLocal()

    try:

        prediction = (
            db.query(Prediction)
            .filter(
                Prediction.patient_id == patient_id
            )
            .order_by(
                Prediction.id.desc()
            )
            .first()
        )

        if not prediction:
            raise HTTPException(
                status_code=404,
                detail="No waveform found"
            )

        return {
            "signal": json.loads(
                prediction.waveform
            )
        }

    finally:
        db.close()

@app.get("/sdp-trend/{patient_id}")
def sdp_trend(patient_id: str):

    db = SessionLocal()

    try:

        predictions = (
            db.query(Prediction)
            .filter(
                Prediction.patient_id == patient_id
            )
            .order_by(
                Prediction.id.asc()
            )
            .limit(50)
            .all()
        )

        return [
            {
                "sdp": p.sdp,
                "timestamp": p.timestamp
            }
            for p in predictions
        ]

    finally:
        db.close()



class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    gestational_week: int

@app.post("/patients")
def add_patient(patient: PatientCreate):

    db = SessionLocal()

    try:

        existing_patient = (
            db.query(Patient)
            .filter(
                Patient.patient_id == patient.patient_id
            )
            .first()
        )

        if existing_patient:
            raise HTTPException(
                status_code=400,
                detail="Patient already exists"
            )

        new_patient = Patient(
            patient_id=patient.patient_id,
            name=patient.name,
            age=patient.age,
            gestational_week=patient.gestational_week
        )

        db.add(new_patient)
        db.commit()

        return {
            "message": "Patient added successfully"
        }

    finally:
        db.close()