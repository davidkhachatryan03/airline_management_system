from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.common.exceptions import *
import logging

def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(InexistentFlight)
    async def inexistent_flight_handler(request: Request, exc: InexistentFlight):
        return JSONResponse(
            status_code=404, 
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )

    @app.exception_handler(BlacklistedPassenger)
    async def blacklisted_passenger_handler(request: Request, exc: BlacklistedPassenger):
        return JSONResponse(
            status_code=403,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )

    @app.exception_handler(FullFlight)
    async def full_flight_handler(request: Request, exc: FullFlight):
        return JSONResponse(
            status_code=409, 
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )

    @app.exception_handler(NotScheduledFlight)
    async def not_scheduled_flight_handler(request: Request, exc: NotScheduledFlight):
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc) 
            }
        )

    @app.exception_handler(InvalidData)
    async def invalid_data_handler(request: Request, exc: InvalidData):
        return JSONResponse(
            status_code=400,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        logging.error(f"CRITICAL INFRASTRUCTURE ERROR: {str(exc)}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )