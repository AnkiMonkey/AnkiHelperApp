import fitz
from PIL import Image
import os

# Prompt user to input PDF file name without extension
pdffile_name = input("Enter the PDF file name (without extension): ")

# Add ".pdf" extension to the provided file name
pdffile = pdffile_name + ".pdf"

# Create a new folder named "jpg_from_name_of_pdf" to store JPEG images if it doesn't exist
jpg_folder = f"jpg_from_{pdffile_name}"
os.makedirs(jpg_folder, exist_ok=True)

doc = fitz.open(pdffile)

# Setting quality to 100 to omit any error in ANKI
for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    pix = page.get_pixmap()
    output = os.path.join(jpg_folder, f"{page_number + 1}.jpg")  # Save JPEG images within the "jpg_from_name_of_pdf" folder
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img.save(output, quality=100)  # Set quality to 100 for maximum quality

doc.close()
