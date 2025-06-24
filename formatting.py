#formatting.py

import sys
import re
import os

def clean_questions(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # --- PHASE 1: Preprocessing ---
    text = re.sub(r'\[Page.*?\]', '', text)               # Remove page markers
    text = re.sub(r'©', '', text)                         # Remove copyright symbols
    text = re.sub(r'\s+', ' ', text).strip()              # Collapse whitespace
    text = re.sub(r'(Question\s*\d+)', r'\n###\1', text)  # Add marker before each question

    # --- PHASE 2: Chunking ---
    chunks = text.split('###')[1:]  # Ignore empty part before first question

    final_output = ""
    current_qnum = 1
    skipped_count = 0

    for chunk in chunks:
        chunk = chunk.strip()

        # ❌ Skip image-only questions
        if re.search(r'Options\s*:\s*A\.\s*B\.\s*C\.\s*D\.', chunk, re.IGNORECASE):
            skipped_count += 1
            continue

        # 🧼 Remove 'Solution: ...'
        chunk = re.sub(r'Solution\s*:\s*.*$', '', chunk, flags=re.IGNORECASE)

        # 🧼 Remove Answer label (but store the answer)
        answer_match = re.search(r'Answer\s*:\s*([A-D])', chunk)
        answer = answer_match.group(1) if answer_match else "Not found"
        chunk = re.sub(r'Answer\s*:\s*[A-D]', '', chunk).strip()

        # 🔢 Remove any 'Question X' from inside
        chunk = re.sub(r'^Question\s*\d+\s*', '', chunk).strip()

        # ✅ Write renumbered question
        final_output += f"Question{current_qnum} {chunk} Answer: {answer}\n"
        current_qnum += 1

    # Save cleaned output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_output)

    # Return new total count of questions
    return current_qnum - 1


# === Run ===
if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    total_questions = clean_questions(input_path, output_path)
    print(total_questions)
