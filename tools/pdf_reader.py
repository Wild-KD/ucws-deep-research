"""Extract text from PDF files using PyMuPDF."""
from pathlib import Path


class PDFReaderTool:
    name = "pdf_reader"
    description = "Extract text content from a PDF file."
    input_schema = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the PDF file",
            },
            "pages": {
                "type": "string",
                "description": "Page range, e.g. '1-10' or '5' (default: all)",
                "default": "all",
            },
        },
        "required": ["file_path"],
    }

    async def execute(self, file_path: str, pages: str = "all") -> str:
        import fitz  # PyMuPDF

        path = Path(file_path)
        if not path.exists():
            return f"Error: File not found: {file_path}"

        doc = fitz.open(str(path))
        total = len(doc)

        if pages == "all":
            page_range = range(total)
        elif "-" in pages:
            start, end = pages.split("-")
            page_range = range(int(start) - 1, min(int(end), total))
        else:
            page_range = [int(pages) - 1]

        texts = []
        for i in page_range:
            if 0 <= i < total:
                page = doc[i]
                texts.append(f"--- Page {i + 1} ---\n{page.get_text()}")

        doc.close()
        return "\n\n".join(texts)
