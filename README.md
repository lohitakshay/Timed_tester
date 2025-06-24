# PDF-to-Timed-Practice-Test Pipeline

This is a **vibe-coded** personal project built to help create timed practice tests from PDF question banks — originally made for my sister, who needed a better way to practice her questions with or without solutions.

---

## What does this do?

The scripts form a pipeline to convert PDFs of practice questions into a structured format for generating timed tests and explainable solutions using GPT.

**Key features:**
- Converts PDF to DOCX
- Extracts raw text from DOCX, including OCR on image-only pages
- Cleans and formats questions (removes unwanted text, renumbers questions)
- Extracts multiple-choice questions (MCQs) with options and answers
- Outputs JSONL files ready for use in testing or GPT-based solution generation

---

## Why am I proud of this?

I had no prior web or backend experience. Using GPT and Perplexity as coding copilots, I learned to build this from scratch.  
While the project wasn’t perfect and I eventually scrapped the full app, the learning journey was invaluable — from raw PDF processing to structured question extraction.

---

## How to use

1. Put your PDFs in the `physics/pdfs/` or your wish folder.  
2. Adjust the Python interpreter path in the main script if needed (`PYTHON_BIN`).  
3. Run the pipeline script to process all PDFs:

```bash
python scripts/run_pipeline.py
