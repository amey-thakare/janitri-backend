from pydantic import BaseModel
from typing import List

class WaveformRequest(BaseModel):
    signal: List[float]
    patient_id: str
    device_id: str
    timestamp: str


class PatientCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    gestational_week: int


class PatientResponse(BaseModel):
    patient_id: str
    name: str
    age: int
    gestational_week: int

    class Config:
        from_attributes = True