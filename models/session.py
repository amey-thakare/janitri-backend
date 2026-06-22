from sqlalchemy import Column, Integer, String, Text
from models.base import Base


class Session(Base):

    __tablename__ = "sessions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    patient_id = Column(
        String(50)
    )

    start_time = Column(
        String(50)
    )

    end_time = Column(
        String(50)
    )

    sdp_values = Column(
        Text
    )