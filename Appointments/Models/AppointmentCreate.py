from pydantic import BaseModel, field_validator

class AppointmentCreate(BaseModel):
    name: str
    time: str

    @field_validator("name")
    @classmethod
    def name_min_length(cls, value):
        if len(value) <= 3:
            raise ValueError("Name must be at least 4 characters long")
        return value
