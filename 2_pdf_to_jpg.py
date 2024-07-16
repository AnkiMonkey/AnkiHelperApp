import fitz  # PyMuPDF
from PIL import Image
import os

# Prompt user to input PDF file name without extension
subject_name = input("Enter the abbreviation of the subject (without extension): ")

pdffile_name = input("Enter the PDF file name (without extension): ")

# Prompt user to specify if pages are from Vorlesung or Praktikum
print("Please choose the type of content:")
print("1. Vorlesung (Lecture)")
print("2. Praktikum (Practical)")
content_type_choice = input("Enter the number of your choice: ")

# Validate user input for content type
if content_type_choice not in ['1', '2']:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

# Determine if it's Vorlesung (V) or Praktikum (P)
if content_type_choice == '1':
    content_type = 'V'
elif content_type_choice == '2':
    content_type = 'P'

# Prompt user to input a number of Vorlesung or Praktikum
number_input = input(f"Enter the number of {content_type} (without extension as 01, 02... 10): ")

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
    
    # Determine the content type prefix (V or P)
    content_prefix = f"{content_type}_{number_input_padded}"
    
    # Ensure the page_number is zero-padded to two digits
    page_number_padded = f"S_{page_number + 1:02}"
    
    # Construct the output file name based on the pattern V_##-S_## or P_##-S_## with zero-padding
    output = os.path.join(jpg_folder, f"{subject_name}_{content_prefix}_{page_number_padded}.jpg")
    
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # No resizing or cropping, keep original resolution
    img.save(output, quality=100)  # Set quality to 100 for maximum quality

print('The jpg files are exported')
doc.close()
