from fastapi import APIRouter, Depends

from src.api.schemas import DocumentRequest, DocumentResponse
from src.common import DBManager
from src.core.units_of_work import RegisterDocumentUoW
from src.core.use_cases import RegisterDocument, RegisterDocumentValidator
from src.core.validators import BaseValidator

router = APIRouter(prefix="/api/documents", tags=["Documents"])


def create_register_document() -> RegisterDocument:
    db_manager = DBManager()
    base_validator = BaseValidator()

    return RegisterDocument(
        RegisterDocumentUoW(db_manager), RegisterDocumentValidator(base_validator)
    )


@router.post("/", response_model=DocumentResponse)
def register_document(
    document_request: DocumentRequest,
    register_document: RegisterDocument = Depends(create_register_document),
):
    document_response = register_document.execute(document_request)

    return document_response
