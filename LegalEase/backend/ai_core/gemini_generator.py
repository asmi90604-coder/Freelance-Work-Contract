from __future__ import annotations

from typing import Any

from backend.core.config import settings

class GeminiDocumentGenerator:
    """
    Gemini adapter.

    The project documentation specifies Gemini 1.5 Pro and the Google
    Generative AI SDK. The import is kept inside this class so the rest
    of the application can start and report a useful configuration error
    instead of failing during module import.
    """

    def __init__(self) -> None:
        self.model_name = settings.GEMINI_MODEL
        self._model: Any = None

        if not settings.GEMINI_API_KEY:
            return

        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise RuntimeError(
                "google-generativeai is not installed. Run: pip install -r requirements.txt"
            ) from exc

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._model = genai.GenerativeModel(self.model_name)

    @property
    def configured(self) -> bool:
        return self._model is not None

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:
        if not self.configured:
            raise RuntimeError(
                "Gemini is not configured. Add GEMINI_API_KEY to your .env file."
            )

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Create a professional DRAFT of the requested legal document using only
the information supplied below.

DOCUMENT TYPE:
{document_type}

PARTIES INVOLVED:
{parties}

EFFECTIVE DATE:
{dates}

TERMS AND CONDITIONS:
{terms}

INSTRUCTIONS:
1. Clearly title the document.
2. Use structured sections appropriate to the document type.
3. Include the parties and effective date.
4. Include appropriate clauses such as definitions, obligations,
   payment/compensation when relevant, confidentiality, termination,
   governing law, notices, and signatures when appropriate.
5. Do not invent names, dates, addresses, prices, laws, jurisdictions,
   or other facts that were not supplied.
6. Use [TO BE COMPLETED] where important information is missing.
7. Keep the supplied terms intact in meaning.
8. Return only the draft document.
9. Mark the document as "AI-GENERATED DRAFT".
10. Include a short final notice stating that the draft should be reviewed
    by a qualified legal professional before use.

This tool provides drafting assistance and is not a substitute for legal advice.
"""

        try:
            response = self._model.generate_content(prompt)
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
