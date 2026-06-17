from sqlalchemy import Column, String, Integer
from models.base import Base

class Patient(Base):

    __tablename__ = "patients"

    patient_id = Column(
        String(50),
        primary_key=True
    )

    name = Column(
        String(100)
    )

    age = Column(
        Integer
    )

    gestational_week = Column(
        Integer
    )