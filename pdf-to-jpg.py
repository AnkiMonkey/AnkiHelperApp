import fitz  # PyMuPDF
from PIL import Image
import os

# Prompt user to input PDF file name without extension
pdffile_name = input("Enter the PDF file name (without extension): ")

# Prompt user to input a number of Vorlesung
number_input = input("Enter the number of Vorlesung: ")

# Add ".pdf" extension to the provided file name
pdffile = pdffile_name + ".pdf"

# Create a new folder named "jpg_from_name_of_pdf" to store JPEG images if it doesn't exist
jpg_folder = f"jpg_from_{pdffile_name}"
os.makedirs(jpg_folder, exist_ok=True)

doc = fitz.open(pdffile)

# Ensure the number_input is zero-padded to two digits
number_input_padded = f"{int(number_input):02}"

for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    
    # Use default matrix to keep the same resolution as the PDF
    pix = page.get_pixmap()
    
    # Ensure the page_number is zero-padded to two digits
    page_number_padded = f"{page_number + 1:02}"
    
    # Construct the output file name based on the pattern V_##-S_## with zero-padding
    output = os.path.join(jpg_folder, f"V_{number_input_padded}-S_{page_number_padded}.jpg")
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # No resizing or cropping, keep original resolution
    img.save(output, quality=100)  # Set quality to 100 for maximum quality

print('The jpg files are exported')
doc.close()
