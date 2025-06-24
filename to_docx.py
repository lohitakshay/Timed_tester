#to_docx.py


import sys
from pdf2docx import Converter

pdf_file = sys.argv[1]
docx_file = sys.argv[2]
# Create converter object
cv = Converter(pdf_file)

# Convert
cv.convert(docx_file, start=0, end=None)  # You can set page range
cv.close()
