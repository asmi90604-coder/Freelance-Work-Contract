from backend.services.export_service import format_docx, format_pdf

def test_docx_export():
    data = format_docx("DRAFT\n\nThis is a test.", "Test Agreement")
    assert data[:2] == b"PK"

def test_pdf_export():
    data = format_pdf("DRAFT\n\nThis is a test.", "Test Agreement")
    assert data.startswith(b"%PDF")
