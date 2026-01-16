from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Database
from app.routers import doctor_router
from app.db.db import engine
from app.db.base import Base
# Routers
from app.routers import patient_router, appointment_router, visiting_room


# Database initialization

# This will create all tables defined in SQLAlchemy models
# ONLY if they do not already exist
Base.metadata.create_all(bind = engine)



# FastAPI application instance

app = FastAPI(
    title = "Welcome to the Medical Clinic API",
    description = "API for managing doctors, patients, appointments and visiting rooms",
    version = "1.0.0"
)


# CORS configuration

# This allows the frontend (e.g. Vue, React, Quasar) to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # In production, replace with frontend domain
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


# API Routers

# Each router is responsible for a specific domain entity
app.include_router(doctor_router.router, prefix = "/doctors", tags = ["Doctors"])
app.include_router(patient_router.router, prefix = "/patients", tags = ["Patients"])
app.include_router(appointment_router.router, prefix = "/appointments", tags = ["Appointments"])
app.include_router(visiting_room.router, prefix = "/visiting-rooms", tags = ["Visiting Rooms"])



# Health check endpoint

@app.get("/", tags = ["Health Check"])
def root():
    
    # Simple endpoint to verify that the API is running.
    
    return {
        "status": "ok",
        "message": "Medical Clinic API is running"
    }
