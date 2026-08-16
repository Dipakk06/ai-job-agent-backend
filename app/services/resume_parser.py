from pathlib import Path
from pypdf import PdfReader


def extract_resume_text(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Currently only PDF resumes are supported.")

    reader = PdfReader(str(path))
    text = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            text.append(page_text)

    result = "\n".join(text).strip()
    if not result:
        raise ValueError("No extractable text was found in the PDF.")
    return result
