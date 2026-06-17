from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text
)

from models.base import Base

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patient_id = Column(
        String(50)
    )

    device_id = Column(
        String(50)
    )

    sdp = Column(
        Float
    )

    status = Column(
        String(20)
    )

    waveform = Column(
        Text
    )

    timestamp = Column(
        String(50)
    )