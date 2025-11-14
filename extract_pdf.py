import PyPDF2
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# Open the PDF file
pdf_path = r"c:\dev\GT\ISYE6202_Warehousing\CW3\Docs\ISyE 6202 & 6335 Casework 3 FeMoaSa Facility Organization Testbed Fall 2025.pdf"

with open(pdf_path, 'rb') as file:
    # Create PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)
    
    # Get number of pages
    num_pages = len(pdf_reader.pages)
    print(f"Total pages: {num_pages}\n")
    
    # Extract text from all pages
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        print(f"--- Page {page_num + 1} ---")
        print(text)
        print("\n" + "="*80 + "\n")
