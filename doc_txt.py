#doc_txt.py

import sys
import fitz
import pytesseract
import tempfile
import os
import re
from pdf2image import convert_from_path

# 🛠️ CLI Arguments
DOCX_PATH = sys.argv[1]
RAW_OUTPUT = sys.argv[2]

# 🧠 Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 📂 Ensure output folder exists
os.makedirs(os.path.dirname(RAW_OUTPUT), exist_ok=True)

# 🔒 Check input file
if not os.path.exists(DOCX_PATH):
    print(f"❌ File not found: {DOCX_PATH}")
    sys.exit(1)

def extract_all_text():
    doc = fitz.open(DOCX_PATH)
    combined_text = ""

    for page_num in range(doc.page_count):
        print(f"\n📄 Processing Page {page_num + 1}/{doc.page_count}")
        page = doc.load_page(page_num)
        text = page.get_text().strip()

        if not text:
            print("🔍 No selectable text — running OCR...")
            with tempfile.TemporaryDirectory() as tmpdir:
                img = convert_from_path(
                    DOCX_PATH,
                    dpi=300,
                    first_page=page_num + 1,
                    last_page=page_num + 1,
                    output_folder=tmpdir
                )[0]
                text = pytesseract.image_to_string(img)

        text = re.sub(r'-{5,}', '', text)
        combined_text += f"\n[Page {page_num + 1}]\n{text.strip()}\n"

    with open(RAW_OUTPUT, "w", encoding="utf-8") as f:
        f.write(combined_text)

    print(f"\n✅ DONE! Extracted text saved to: {RAW_OUTPUT}")

if __name__ == "__main__":
    extract_all_text()
