from pydantic import BaseModel


# Base schema (shared fields)
class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    availability: str


# CREATE
class DoctorCreate(DoctorBase):
    pass


# UPDATE
class DoctorUpdate(BaseModel):
    full_name: str | None = None
    specialization: str | None = None
    availability: str | None = None


# READ (response)
class DoctorRead(DoctorBase):
    id: int

    class Config:
        from_attributes = True