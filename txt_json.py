#txt_json.py

import os
import re
import json
import sys
import formatting  # Make sure this exists

def extract_mcqs_from_cleaned_text(cleaned_text):
    lines = cleaned_text.strip().splitlines()
    mcqs = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match question number
        q_match = re.match(r"Question\s*(\d+)\s+", line, flags=re.IGNORECASE)
        if not q_match:
            continue
        qnum = q_match.group(1)

        # Extract answer
        a_match = re.search(r"Answer\s*:\s*([A-D])", line, flags=re.IGNORECASE)
        if not a_match:
            continue
        answer = a_match.group(1).strip()

        # Extract year from [NEET xxxx]
        year_match = re.search(r"\[NEET[-\s]*?(\d{4})", line, flags=re.IGNORECASE)
        year = year_match.group(1) if year_match else None

        # Remove leading "QuestionX " and trailing "Answer: X"
        question_body = re.sub(r"^Question\s*\d+\s+", "", line)
        question_body = re.sub(r"Answer\s*:\s*[A-D]\s*$", "", question_body).strip()

        # Remove year tag from question text
        question_body = re.sub(r"\[NEET[-\s]*?\d{4}.*?\]", "", question_body).strip()

        # Split question and options
        parts = re.split(r"Options\s*:\s*", question_body, flags=re.IGNORECASE)
        if len(parts) != 2:
            continue
        question_text, options_text = parts

        # Extract options
        options = re.findall(r"[A-D]\.\s*(.*?)(?=\s+[A-D]\.|$)", options_text, flags=re.DOTALL)
        options = [opt.strip() for opt in options]

        if len(options) == 4:
            mcq_data = {
                "q": qnum,
                "question": question_text.strip(),
                "options": options,
                "answer": answer
            }
            if year:
                mcq_data["year"] = year
            mcqs.append(mcq_data)

    return mcqs




def save_jsonl(mcqs, path):
    print(f"💾 Writing {len(mcqs)} MCQs to {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in mcqs:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def run_pipeline(raw_txt_path, cleaned_txt_path, jsonl_output_path):
    print("🚀 Starting pipeline...")

    # ✅ Step 1: Clean the raw text and save to cleaned_txt_path
    max_qnum = formatting.clean_questions(raw_txt_path, cleaned_txt_path)
    print(f"🎯 Detected max question number: {max_qnum}")

    attempt = 1
    while True:
        print(f"\n🔁 Attempt {attempt}: extracting MCQs from cleaned text...")
        with open(cleaned_txt_path, "r", encoding="utf-8") as f:
            cleaned_text = f.read()

        mcqs = extract_mcqs_from_cleaned_text(cleaned_text)
        print(f"🔍 Extracted {len(mcqs)} MCQs")

        if len(mcqs) == max_qnum:
            print("✅ Question count matches expected.")
            save_jsonl(mcqs, jsonl_output_path)
            break
        else:
            print(f"⚠️ Expected {max_qnum}, but got {len(mcqs)}. Retrying...")
            attempt += 1
            if attempt > 5:
                print("🛑 Max attempts reached. Saving partial result.")
                save_jsonl(mcqs, jsonl_output_path)
                break

if __name__ == "__main__":
    raw_txt = sys.argv[1]
    cleaned_txt = sys.argv[2]
    jsonl_out = sys.argv[3]
    run_pipeline(raw_txt, cleaned_txt, jsonl_out)
