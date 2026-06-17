import json
import requests
import random
import time
from datetime import datetime

API_URL = "https://janitri-backend-3yn0.onrender.com/upload-waveform"

DEVICE_ID = "JAN001"
PATIENT_ID = "P001"

# Load waveforms
with open("sample_waveforms.json", "r") as f:
    waveform_data = json.load(f)

signals = waveform_data["signals"]

print(f"Loaded {len(signals)} waveforms")

while True:

    signal = random.choice(signals)

    payload = {
        "device_id": DEVICE_ID,
        "patient_id": PATIENT_ID,
        "timestamp": datetime.utcnow().isoformat(),
        "signal": signal
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=20
        )

        print("\n========================")
        print("Device:", DEVICE_ID)
        print("Patient:", PATIENT_ID)
        print("Samples:", len(signal))
        print("Status Code:", response.status_code)

        if response.status_code == 200:
            print("Server Response:", response.json())
        else:
            print("Error:", response.text)

    except Exception as e:
        print("Connection Error:", e)

    time.sleep(10)