
from io import BytesIO
from html import escape

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from fpdf import FPDF


# =========================================================
# TXT EXPORT
# =========================================================

def format_txt(document_text: str) -> bytes:
    """
    Convert the generated legal document into a TXT file.
    """
    return document_text.encode("utf-8")


# =========================================================
# HTML PREVIEW
# =========================================================

def format_html_preview(document_text: str) -> str:
    """
    Convert legal document text into simple HTML for Streamlit preview.
    """

    escaped_text = escape(document_text)

    # Preserve line breaks
    html_text = escaped_text.replace("\n", "<br>")

    return f"""
    <div style="
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        color: #1e293b;
        font-family: 'Times New Roman', serif;
        line-height: 1.7;
        font-size: 16px;
        max-height: 600px;
        overflow-y: auto;
    ">
        {html_text}
    </div>
    """


# =========================================================
# DOCX EXPORT
# =========================================================

def format_docx(document_text: str, document_type: str = "Legal Document") -> bytes:
    """
    Create a DOCX legal document.
    """

    document = Document()

    # Default font
    styles = document.styles
    normal_style = styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)

    # Title
    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    title_run = title.add_run(document_type)
    title_run.bold = True
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)

    document.add_paragraph()

    # Document content
    for line in document_text.splitlines():

        line = line.strip()

        if not line:
            document.add_paragraph()
            continue

        paragraph = document.add_paragraph()

        run = paragraph.add_run(line)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)

    # Footer
    section = document.sections[0]
    footer = section.footer

    footer_paragraph = footer.paragraphs[0]
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_run = footer_paragraph.add_run(
        "LegalEase - AI-Powered Legal Document Generator"
    )
    footer_run.font.name = "Times New Roman"
    footer_run.font.size = Pt(9)

    # Save to memory
    output = BytesIO()
    document.save(output)

    output.seek(0)

    return output.getvalue()


# =========================================================
# PDF EXPORT
# =========================================================

class LegalEasePDF(FPDF):

    def header(self):
        self.set_font("Times", "B", 14)
        self.cell(
            0,
            10,
            "LegalEase",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        self.set_font("Times", "", 9)
        self.cell(
            0,
            6,
            "AI-Powered Legal Document Generator",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        self.ln(5)

    def footer(self):
        self.set_y(-15)

        self.set_font("Times", "", 8)

        self.cell(
            0,
            10,
            f"Page {self.page_no()}",
            align="C",
        )


def format_pdf(
    document_text: str,
    document_type: str = "Legal Document",
) -> bytes:
    """
    Create a PDF legal document.
    """

    pdf = LegalEasePDF()

    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_page()

    # Document title
    pdf.set_font("Times", "B", 16)

    pdf.multi_cell(
        0,
        10,
        document_type,
        align="C",
    )

    pdf.ln(5)

    # Document body
    pdf.set_font("Times", "", 12)

    for line in document_text.splitlines():

        line = line.strip()

        if not line:
            pdf.ln(5)
            continue

        pdf.multi_cell(
            0,
            7,
            line,
        )

        pdf.ln(1)

    # Return PDF bytes
    return bytes(pdf.output())
