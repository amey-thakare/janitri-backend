# Janitri Backend

AI-powered fetal monitoring backend.

## Tech Stack

- Flask
- PostgreSQL
- SQLAlchemy
- TensorFlow CNN

## Features

- Patient Management
- Waveform Upload API
- SDP Prediction
- Prediction History
- SDP Trend Analysis

## Setup

Create virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run backend:

python3 app.py

Server:

http://127.0.0.1:8000


GET /patients
GET /latest/P123
GET /history/P123
GET /waveform/P123
POST /upload-waveform
