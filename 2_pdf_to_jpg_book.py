import fitz  # PyMuPDF
from PIL import Image
import os

# Prompt user to input PDF file name without extension
subject_name = input("Enter the abbreviation of the subject (without extension): ")
item_type = "BOOK"
pdffile_name = input("Enter the PDF file name (without extension): ")

# Add ".pdf" extension to the provided file name
pdffile = pdffile_name + ".pdf"

# Create a new folder named "jpg_from_name_of_pdf" to store JPEG images if it doesn't exist
jpg_folder = f"jpg_from_{pdffile_name}"
os.makedirs(jpg_folder, exist_ok=True)

doc = fitz.open(pdffile)

for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    
    # Use default matrix to keep the same resolution as the PDF
    pix = page.get_pixmap()
 
    
    # Ensure the page_number is zero-padded to two digits
    page_number_padded = f"S_{page_number + 1:02}"
    
    # Construct the output file name based on the pattern V_##-S_## or P_##-S_## with zero-padding
    output = os.path.join(jpg_folder, f"{item_type}_{subject_name}_{page_number_padded}.jpg")
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # No resizing or cropping, keep original resolution
    img.save(output, quality=100)  # Set quality to 100 for maximum quality

print('The jpg files are exported')
doc.close()
