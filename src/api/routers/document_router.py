from fastapi import APIRouter, Depends

from src.api.schemas import DocumentRequest, DocumentResponse
from src.common import DBManager
from src.core.validators import DocumentValidator, PassengerValidator
from src.core.use_cases import RegisterDocument
from src.core.units_of_work import RegisterDocumentUoW

router = APIRouter(prefix="/api/documents", tags=["Documents"])

def get_document_registrar() -> RegisterDocument:
    db_manager = DBManager()
    document_validator = DocumentValidator()
    passenger_validator = PassengerValidator()

    return RegisterDocument(RegisterDocumentUoW(db_manager), passenger_validator, document_validator)

@router.post("/", response_model=DocumentResponse)
def register_document(document_request: DocumentRequest, document_registrar: RegisterDocument = Depends(get_document_registrar)):
    document_response = document_registrar.execute(document_request)

    return document_response