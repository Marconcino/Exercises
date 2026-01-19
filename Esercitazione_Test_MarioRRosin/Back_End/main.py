from fastapi import FastAPI
from app.database.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware
    
from app.routers.table_router import router as table_router
from app.routers.client_router import router as client_router
from app.routers.booking_router import router as booking_router

app = FastAPI(title = "FlyingBees Pizza - System Booking API", version = "1.0.0", 
              description = "REST API for managing restaurant tables, clients and bookings")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(table_router)
app.include_router(client_router)
app.include_router(booking_router)

# CORS settings to check with frontend running on localhost:9000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
