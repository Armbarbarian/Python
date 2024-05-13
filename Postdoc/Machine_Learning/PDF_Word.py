import pdf2docx

# Open the PDF file
pdf_file = open('2924Abramson_Alphafold3.pdf', 'rb')

# Create a new Word document from the PDF
doc = pdf2docx.parse(pdf_file)

# Save the Word document
doc.save('2924Abramson_Alphafold3.docx')

print("PDF successfully converted to Word document.")