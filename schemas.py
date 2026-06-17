from pydantic import BaseModel
from typing import List

class WaveformRequest(BaseModel):
    signal: List[float]
    patient_id: str
    device_id: str
    timestamp: str