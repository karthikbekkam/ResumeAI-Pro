import os
import fitz  # PyMuPDF
import docx

class FileParser:
    @staticmethod
    def extract_text(file_path):
        """
        Extract raw text from PDF or DOCX/DOC files using PyMuPDF and python-docx.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = file_path.rsplit(".", 1)[-1].lower()

        if ext == "pdf":
            return FileParser._extract_from_pdf(file_path)
        elif ext in ["docx", "doc"]:
            return FileParser._extract_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _extract_from_pdf(file_path):
        text_content = []
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text_content.append(page.get_text())
            doc.close()
            full_text = "\n".join(text_content).strip()
            return full_text
        except Exception as e:
            raise RuntimeError(f"Error parsing PDF file: {str(e)}")

    @staticmethod
    def _extract_from_docx(file_path):
        try:
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text.strip())
            
            # Also extract text inside tables if any
            for table in doc.tables:
                for row in table.rows:
                    row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_data:
                        full_text.append(" | ".join(row_data))

            return "\n".join(full_text).strip()
        except Exception as e:
            # Fallback text extraction if docx library fails on older doc format
            raise RuntimeError(f"Error parsing DOCX file: {str(e)}")
