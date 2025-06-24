import os
import subprocess
import shutil
from glob import glob

# 🐍 Python interpreter path (adjust if needed)
PYTHON_BIN = "venv/Scripts/python"

# 📁 Input and output directories
pdf_dir = "physics/pdfs"
intermediate_dirs = ["docs", "txt_files", "cleaned", "json_files"]
final_output_dir = "physics/final"

# 🔄 Ensure final output folder exists
os.makedirs(final_output_dir, exist_ok=True)

# 📥 Get list of all PDFs to process
print(f"🔍 Looking for PDFs in: {pdf_dir}")
pdf_files = sorted(glob(os.path.join(pdf_dir, "*.pdf")))

if not pdf_files:
    print("❌ No PDF files found in 'physics/pdfs' directory.")
    exit()

print(f"📦 Found {len(pdf_files)} PDF file(s) to process.\n")

# 🚀 Process each PDF file one-by-one
for pdf_path in pdf_files:
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    print(f"{'='*60}")
    print(f"🚀 Starting pipeline for: {base.upper()}")
    print(f"📄 Input PDF: {pdf_path}")

    # Define paths for intermediate outputs
    docx_path = f"docs/{base}.docx"
    txt_path = f"txt_files/{base}.txt"
    cleaned_path = f"cleaned/{base}.txt"
    jsonl_path = f"json_files/{base}.jsonl"

    # Define path for final JSONL output
    final_json_path = os.path.join(final_output_dir, f"{base}.jsonl")

    try:
        # STEP 1: PDF → DOCX
        print("➡️ Step 1: Converting PDF to DOCX...")
        print(f"    Running: {PYTHON_BIN} scripts/to_docx.py {pdf_path} {docx_path}")
        subprocess.run([PYTHON_BIN, "scripts/to_docx.py", pdf_path, docx_path], check=True)
        print(f"    ✅ DOCX saved to: {docx_path}")

        # STEP 2: DOCX → TXT
        print("➡️ Step 2: Extracting raw text from DOCX...")
        print(f"    Running: {PYTHON_BIN} scripts/doc_txt.py {docx_path} {txt_path}")
        subprocess.run([PYTHON_BIN, "scripts/doc_txt.py", docx_path, txt_path], check=True)
        print(f"    ✅ Raw text saved to: {txt_path}")

        # STEP 3: Clean/Format TXT
        print("➡️ Step 3: Cleaning and formatting text...")
        print(f"    Running: {PYTHON_BIN} scripts/formatting.py {txt_path} {cleaned_path}")
        subprocess.run([PYTHON_BIN, "scripts/formatting.py", txt_path, cleaned_path], check=True)
        print(f"    ✅ Cleaned text saved to: {cleaned_path}")

        # STEP 4: Generate JSONL
        print("➡️ Step 4: Generating JSONL from cleaned text...")
        print(f"    Running: {PYTHON_BIN} scripts/txt_json.py {txt_path} {cleaned_path} {jsonl_path}")
        subprocess.run([PYTHON_BIN, "scripts/txt_json.py", txt_path, cleaned_path, jsonl_path], check=True)
        print(f"    ✅ JSONL created at: {jsonl_path}")

        # STEP 5: Move final output to physics/final
        print(f"➡️ Step 5: Moving final JSONL to: {final_json_path}")
        shutil.move(jsonl_path, final_json_path)
        print(f"    ✅ Final JSONL available at: {final_json_path}")

    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR during processing of {base}:")
        print(e)
        continue

    # STEP 6: Cleanup intermediate files
    print("🧹 Cleaning up intermediate files...")
    for path in [docx_path, txt_path, cleaned_path, jsonl_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"    🗑️ Deleted: {path}")
        else:
            print(f"    ⚠️ Not found (skipped): {path}")

    print(f"✅ COMPLETED: {base.upper()}\n")

print(f"{'='*60}")
print("🎉 All PDFs processed successfully!")
print(f"📁 Final outputs saved in: {final_output_dir}")
