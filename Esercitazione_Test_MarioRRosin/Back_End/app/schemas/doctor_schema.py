from pydantic import BaseModel


# Base schema (shared fields)
class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    specialization: str
    availability: str


# CREATE
class DoctorCreate(DoctorBase):
    pass


# UPDATE
class DoctorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    specialization: str | None = None
    availability: str | None = None


# READ (response)
class DoctorRead(DoctorBase):
    id: int

    class Config:
        from_attributes = True
