from fastapi import FastAPI

from src.api.error_handlers import setup_exception_handlers
from src.api.routers import booking_router, document_router, flight_router

app = FastAPI(
    title=" Booking API", description="API for booking's system", version="1.0.0"
)

setup_exception_handlers(app)

app.include_router(booking_router.router)
app.include_router(document_router.router)
app.include_router(flight_router.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "The server is working."}
