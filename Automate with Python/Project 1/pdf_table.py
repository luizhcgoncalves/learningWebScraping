# pip install tk
# pip install ghostscript
# pip install camelot-py
# pip install opencv-python
# pip install PdfReader
import camelot

# Fails with PyPDF2.errors.DeprecationError: PdfFileReader is deprecated and was removed in PyPDF2 3.0.0. Use PdfReader instead
tables = camelot.read_pdf('foo.pdf', pages='1')

# export all tables to a .zip file
tables.export('foo.csv', f='csv', compress=True)

# export specific table to file
tables[0].to_csv('foo.csv')