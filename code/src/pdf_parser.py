class PDFParser:
    def __init__(self):
        pass

    def extract_ecis_number(self, pdf_path):
        import PyPDF2

        ecis_number = None
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        # Assuming ECIS number follows a specific pattern, e.g., "ECIS: 123456"
                        import re
                        match = re.search(r'ECIS:\s*(\d+)', text)
                        if match:
                            ecis_number = match.group(1)
                            break
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}")

        return ecis_number