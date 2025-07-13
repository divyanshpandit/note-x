# app/pdf_generator.py (alternative)
import pdfkit, uuid, tempfile, pathlib

def generate_pdf_from_markdown(md_text: str) -> str:
    import markdown
    html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    out_path = pathlib.Path(tempfile.gettempdir()) / f"{uuid.uuid4()}.pdf"
    pdfkit.from_string(html, str(out_path), options={"quiet": ""})
    return str(out_path)
