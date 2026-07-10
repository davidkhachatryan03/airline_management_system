from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.exceptions import MultipleExceptionsError, InexistentFlight, InexistentPassenger

def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(MultipleExceptionsError)
    async def multiple_exceptions_handler(request: Request, exc: MultipleExceptionsError):
        details = []
        
        for error in exc.exceptions:
            specific_status = getattr(error.__class__, 'status_code', 400)
            
            details.append({
                "error": error.__class__.__name__,
                "message": str(error),
                "internal_code": specific_status
            })

        return JSONResponse(
            status_code=422,
            content={
                "message": "La solicitud no pudo ser procesada debido a conflictos en las reglas de negocio.",
                "total_errors": len(details),
                "details": details
            }
        )
    
    @app.exception_handler(InexistentFlight)
    async def inexistent_flight_handler(request: Request, exc: InexistentFlight):
        return JSONResponse(
            status_code=404, 
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )
    
    @app.exception_handler(InexistentPassenger)
    async def inexistent_passenger_handler(request: Request, exc: InexistentPassenger):
        return JSONResponse(
            status_code=404,
            content={
                "error": exc.__class__.__name__,
                "message": str(exc)
            }
        )