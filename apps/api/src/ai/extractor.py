from pathlib import Path

import docx
import pdfplumber


class ResumeExtractor:
    """
    Extract raw text from supported resume formats.
    """

    @staticmethod
    def extract(file_path: str) -> str:
        path = Path(file_path)

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return ResumeExtractor._extract_pdf(path)

        if suffix == ".docx":
            return ResumeExtractor._extract_docx(path)

        raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _extract_pdf(path: Path) -> str:
        text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text.append(page_text)

        return "\n".join(text)

    @staticmethod
    def _extract_docx(path: Path) -> str:
        document = docx.Document(path)

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )