import pytest
from pydantic import ValidationError
from backend.schemas.documents import DocumentRequest

def test_valid_request():
    item = DocumentRequest(
        document_type="NDA",
        parties="A and B",
        terms="Keep information confidential",
        dates="April 10, 2025",
    )
    assert item.document_type == "NDA"

def test_empty_request_rejected():
    with pytest.raises(ValidationError):
        DocumentRequest(
            document_type="",
            parties="A",
            terms="B",
            dates="C",
        )
