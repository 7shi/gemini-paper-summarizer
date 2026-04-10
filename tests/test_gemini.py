import os

os.environ.setdefault("GEMINI_API_KEY", "test-api-key")

from gp_summarize import gemini


def test_get_upload_mime_type_for_tex_is_plain_text():
    assert gemini.get_upload_mime_type("paper.tex") == "text/plain"


def test_get_upload_mime_type_for_pdf_uses_detected_type():
    assert gemini.get_upload_mime_type("paper.pdf") == "application/pdf"
