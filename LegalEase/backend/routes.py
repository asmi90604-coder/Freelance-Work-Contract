from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.document_service import generate_legal_document

router = APIRouter()


# ---------------------------------------------------------
# Request model
# ---------------------------------------------------------

class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Type of legal document",
    )

    parties: str = Field(
        ...,
        min_length=3,
        max_length=5000,
        description="Parties involved",
    )

    terms: str = Field(
        ...,
        min_length=3,
        max_length=15000,
        description="Terms and conditions",
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Effective date",
    )


# ---------------------------------------------------------
# Generate document
# ---------------------------------------------------------

@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:

        generated_document = generate_legal_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )

        return {
            "success": True,
            "document": generated_document,
            "document_type": request.document_type,
            "message": "Document generated successfully.",
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {str(error)}",
        )