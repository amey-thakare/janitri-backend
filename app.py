from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import os
import json
import database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from config import Config

app.config.from_object(Config)

db = SQLAlchemy(app)
class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(
        db.String(50),
        primary_key=True
    )

    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gestational_week = db.Column(db.Integer)


class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.String(50)
    )

    device_id = db.Column(
        db.String(50)
    )

    sdp = db.Column(
        db.Float
    )

    status = db.Column(
        db.String(20)
    )

    waveform = db.Column(
        db.Text
    )

    timestamp = db.Column(
        db.String(50)
    )

print("Current Directory:", os.getcwd())
print("Model Path:", os.path.abspath("cnn_sdp_model.h5"))

# Load CNN model
model = load_model("cnn_sdp_model.h5", compile=False)

EXPECTED_LENGTH = 5000


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Janitri API Running"
    })


@app.route("/upload-waveform", methods=["POST"])
def upload_waveform():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON received"
            }), 400

        signal = np.array(
            data["signal"],
            dtype=np.float32
        )

        patient_id = data.get("patient_id")
        device_id = data.get("device_id")
        timestamp = data.get("timestamp")

        print("\n========== NEW REQUEST ==========")
        print("Patient:", patient_id)
        print("Device:", device_id)
        print("Length:", len(signal))

        if len(signal) != EXPECTED_LENGTH:
            return jsonify({
                "error":
                f"Expected {EXPECTED_LENGTH} samples, got {len(signal)}"
            }), 400

        # Save original waveform before preprocessing
        original_signal = signal.copy()

        # Same preprocessing used during training
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

        sdp = float(prediction[0][0])

        # Clinical classification
        if sdp < 2:
            status = "ABNORMAL"
        elif sdp > 8:
            status = "ABNORMAL"
        else:
            status = "NORMAL"

        print("SDP =", round(sdp, 2))
        print("Status =", status)

        # Save prediction + waveform to PostgreSQL
        prediction_record = Prediction(
            patient_id=patient_id,
            device_id=device_id,
            sdp=round(sdp, 2),
            status=status,
            waveform=json.dumps(
                original_signal.tolist()
            ),
            timestamp=timestamp
        )

        db.session.add(prediction_record)
        db.session.commit()

        print("Prediction saved to PostgreSQL")

        return jsonify({
            "message": "Waveform received successfully"
        })

    except Exception as e:

        print("\n========== ERROR ==========")
        print(str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/latest/<patient_id>", methods=["GET"])
def latest_prediction(patient_id):

    prediction = (
        Prediction.query
        .filter_by(patient_id=patient_id)
        .order_by(Prediction.id.desc())
        .first()
    )

    if prediction is None:
        return jsonify({
            "error": "No prediction found"
        }), 404

    return jsonify({
        "patient_id": prediction.patient_id,
        "device_id": prediction.device_id,
        "sdp": prediction.sdp,
        "status": prediction.status,
        "timestamp": prediction.timestamp
    })


@app.route("/history/<patient_id>", methods=["GET"])
def history(patient_id):

    predictions = (
        Prediction.query
        .filter_by(patient_id=patient_id)
        .order_by(Prediction.id.desc())
        .limit(20)
        .all()
    )

    return jsonify([
        {
            "sdp": p.sdp,
            "status": p.status,
            "timestamp": p.timestamp
        }
        for p in predictions
    ])

    


@app.route("/waveform/<patient_id>", methods=["GET"])
def waveform(patient_id):

    prediction = (
        Prediction.query
        .filter_by(patient_id=patient_id)
        .order_by(Prediction.id.desc())
        .first()
    )

    if prediction is None:
        return jsonify({
            "error": "No waveform found"
        }), 404

    return jsonify({
        "signal": json.loads(
            prediction.waveform
        )
    })

@app.route("/patients", methods=["GET"])
def get_patients():

    patients = Patient.query.all()

    return jsonify([
        {
            "patient_id": p.patient_id,
            "name": p.name,
            "age": p.age,
            "gestational_week": p.gestational_week
        }
        for p in patients
    ])
@app.route("/sdp-trend/<patient_id>", methods=["GET"])
def sdp_trend(patient_id):

    predictions = (
        Prediction.query
        .filter_by(patient_id=patient_id)
        .order_by(Prediction.id.asc())
        .limit(50)
        .all()
    )

    return jsonify([
        {
            "sdp": p.sdp,
            "timestamp": p.timestamp
        }
        for p in predictions
    ])

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )