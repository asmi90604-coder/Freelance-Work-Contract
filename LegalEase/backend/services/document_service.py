from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.core.config import settings
from backend.schemas.documents import DocumentRequest


class DocumentService:
    def __init__(self) -> None:
        self.generator = GeminiDocumentGenerator()

    def generate(self, request: DocumentRequest) -> str:
        text = self.generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )

        if len(text) > settings.MAX_DOCUMENT_LENGTH:
            text = text[: settings.MAX_DOCUMENT_LENGTH]

        return text


def generate_legal_document(
    document_type: str,
    parties: str,
    terms: str,
    dates: str,
) -> str:
    request = DocumentRequest(
        document_type=document_type,
        parties=parties,
        terms=terms,
        dates=dates,
    )
    return DocumentService().generate(request)
