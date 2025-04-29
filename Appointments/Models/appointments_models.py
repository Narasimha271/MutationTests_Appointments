from sqlalchemy import Column, Integer, String
from Helpers.database import Base
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    time = Column(String, index=True)