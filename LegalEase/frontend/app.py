import os

import requests
import streamlit as st

from dotenv import load_dotenv

from backend.services.export_service import (
    format_docx,
    format_pdf,
    format_txt,
    format_html_preview,
)


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
)


# =========================================================
# STREAMLIT PAGE
# =========================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    color: #172554;
    margin-top: 10px;
    margin-bottom: 0;
}

.main-subtitle {
    text-align: center;
    color: #64748b;
    font-size: 18px;
    margin-bottom: 35px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #172554;
}

.info-box {
    padding: 18px;
    border-radius: 12px;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "document" not in st.session_state:
    st.session_state.document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = "Legal Document"


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="main-subtitle">
AI-Powered Legal Document Generator
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Application Settings")

    backend_url = st.text_input(
        "FastAPI Backend URL",
        value=BACKEND_URL,
    )

    st.divider()

    st.markdown(
        """
### LegalEase Workflow

1. Enter document details
2. Generate with Gemini AI
3. Preview the document
4. Edit the generated text
5. Download TXT / DOCX / PDF
"""
    )

    st.divider()

    st.caption(
        "LegalEase generates AI-assisted drafts. "
        "Review documents before legal use."
    )


# =========================================================
# DOCUMENT INPUT
# =========================================================

st.markdown(
    '<div class="section-title">📝 Document Information</div>',
    unsafe_allow_html=True,
)

st.write(
    "Enter the information needed to generate your legal document."
)

left_column, right_column = st.columns(
    2
)


# ---------------------------------------------------------
# Left column
# ---------------------------------------------------------

with left_column:

    document_type = st.text_input(
        "Document Type",
        placeholder=(
            "Example: Freelance Work Contract"
        ),
        help=(
            "Enter the type of legal document "
            "you want to generate."
        ),
    )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=140,
    )


# ---------------------------------------------------------
# Right column
# ---------------------------------------------------------

with right_column:

    dates = st.text_input(
        "Effective Date",
        placeholder=(
            "Example: April 10, 2025"
        ),
    )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Use semicolons to separate clauses.\n\n"
            "Example:\n"
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=140,
    )


# =========================================================
# GENERATE BUTTON
# =========================================================

st.write("")

generate_button = st.button(
    "🚀 Generate Document",
    type="primary",
    use_container_width=True,
)


if generate_button:

    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    if not document_type.strip():

        st.warning(
            "Please enter a document type."
        )

        st.stop()

    if not parties.strip():

        st.warning(
            "Please enter the parties involved."
        )

        st.stop()

    if not terms.strip():

        st.warning(
            "Please enter the terms and conditions."
        )

        st.stop()

    if not dates.strip():

        st.warning(
            "Please enter the effective date."
        )

        st.stop()

    # -----------------------------------------------------
    # API request
    # -----------------------------------------------------

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates,
    }

    try:

        with st.spinner(
            "🤖 Gemini is generating your legal document..."
        ):

            response = requests.post(
                f"{backend_url.rstrip('/')}/generate",
                json=payload,
                timeout=180,
            )

        # -------------------------------------------------
        # HTTP errors
        # -------------------------------------------------

        response.raise_for_status()

        result = response.json()

        if not result.get("success"):

            st.error(
                "The backend could not generate the document."
            )

            st.stop()

        # -------------------------------------------------
        # Store document
        # -------------------------------------------------

        st.session_state.document = (
            result["document"]
        )

        st.session_state.document_type = (
            document_type
        )

        st.success(
            "✅ Legal document generated successfully!"
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI backend.\n\n"
            "Make sure you started:\n\n"
            "uvicorn main:app --reload"
        )

    except requests.exceptions.Timeout:

        st.error(
            "❌ The request timed out. "
            "Please try again."
        )

    except requests.exceptions.HTTPError as error:

        try:

            error_data = response.json()

            st.error(
                f"Backend error: "
                f"{error_data.get('detail', error)}"
            )

        except Exception:

            st.error(
                f"Backend error: {error}"
            )

    except Exception as error:

        st.error(
            f"Unexpected error: {error}"
        )


# =========================================================
# DOCUMENT RESULT
# =========================================================

if st.session_state.document:

    st.divider()

    st.markdown(
        '<div class="section-title">📄 Generated Document</div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Preview
    # -----------------------------------------------------

    st.subheader(
        "👁️ Document Preview"
    )

    st.markdown(
        format_html_preview(
            st.session_state.document
        ),
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # Editing
    # -----------------------------------------------------

    st.subheader(
        "✏️ Edit Document"
    )

    edited_document = st.text_area(
        "Click inside this area to edit the document",
        value=st.session_state.document,
        height=550,
        key="editable_document",
    )

    st.session_state.document = (
        edited_document
    )

    # -----------------------------------------------------
    # Downloads
    # -----------------------------------------------------

    st.subheader(
        "⬇️ Download / Save"
    )

    try:

        txt_file = format_txt(
            st.session_state.document
        )

        docx_file = format_docx(
            st.session_state.document,
            st.session_state.document_type,
        )

        pdf_file = format_pdf(
            st.session_state.document,
            st.session_state.document_type,
        )

        download_col1, download_col2, download_col3 = (
            st.columns(3)
        )

        with download_col1:

            st.download_button(
                label="📄 Download TXT",
                data=txt_file,
                file_name="LegalEase_Document.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with download_col2:

            st.download_button(
                label="📝 Download DOCX",
                data=docx_file,
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        with download_col3:

            st.download_button(
                label="📕 Download PDF",
                data=pdf_file,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    except Exception as error:

        st.error(
            f"Could not prepare download files: {error}"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
<div style="
    text-align:center;
    color:#64748b;
    padding:20px;
">

<b>LegalEase</b><br>

AI-Powered Legal Document Generator<br><br>

⚠️ AI-generated documents may contain errors or omissions.
Review the document with a qualified legal professional
before relying on it.

</div>
""",
    unsafe_allow_html=True,
)