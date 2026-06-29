from fastapi import FastAPI

from src.api.error_handlers import setup_exception_handlers
from src.api.routers import create_booking_router

app = FastAPI(
    title=" Booking API",
    description="API for booking's system",
    version="1.0.0"
)

setup_exception_handlers(app)

app.include_router(create_booking_router.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "The server is working."}