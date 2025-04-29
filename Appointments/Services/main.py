from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import Models.appointments_models
from Helpers.database import SessionLocal, engine
from pydantic import BaseModel

Models.appointments_models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Pydantic schema for creating an appointment
class AppointmentCreate(BaseModel):
    name: str
    time: str

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /appointments - Create a new appointment
@app.post("/appointments")
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = Models.appointments_models.Appointment(name=appointment.name, time=appointment.time)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

# GET /appointments/{id} - Retrieve an appointment
@app.get("/appointments/{id}")
def get_appointment(id: int, db: Session = Depends(get_db)):
    appointment = db.query(Models.appointments_models.Appointment).filter(Models.appointments_models.Appointment.id == id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# DELETE /appointments/{id} - Cancel an appointment
@app.delete("/appointments/{id}")
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appointment = db.query(Models.appointments_models.Appointment).filter(Models.appointments_models.Appointment.id == id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment cancelled"}