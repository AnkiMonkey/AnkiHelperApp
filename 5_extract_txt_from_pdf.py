import PyPDF2
import os

def list_pdfs_in_directory(directory):
    # List all PDF files in the directory
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

def pdf_to_txt(pdf_file):
    # Extract PDF filename without extension
    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
    
    # Create the txt file with the same name
    txt_file = f"{pdf_name}.txt"
    
    # Open PDF file
    with open(pdf_file, 'rb') as pdf:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(pdf)
        
        # Start writing to the txt file
        with open(txt_file, 'w', encoding='utf-8') as txt:
            # Write the starting line
            txt.write(f"This is the transcript from {pdf_name}\n\n")
            
            # Initialize slide counter
            slide_counter = 1
            
            # Loop through each page in the PDF
            for page in reader.pages:
                # Add the divider and slide number before writing the page content
                txt.write("\n" + "-" * 19 + f"\nThis is slide {slide_counter}\n\n")
                
                # Extract text from the current page
                page_text = page.extract_text() or ""  # Handle cases where text extraction fails
                
                # Write the page text to the txt file
                txt.write(page_text)
                
                # Increment slide counter for the next page
                slide_counter += 1
    
    # Open the txt file after writing
    os.startfile(txt_file)

def main():
    # Get the current directory
    current_directory = os.getcwd()
    
    # Get all the PDF files in the current directory
    pdf_files = list_pdfs_in_directory(current_directory)
    
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    
    # Display the PDF files and let the user choose one
    print("Please choose a PDF to process:")
    for index, pdf in enumerate(pdf_files, start=1):
        print(f"{index}. {pdf}")
    
    # Get the user input
    while True:
        try:
            choice = int(input("Enter the number of the PDF you want to process: "))
            if 1 <= choice <= len(pdf_files):
                break
            else:
                print(f"Please enter a number between 1 and {len(pdf_files)}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Get the selected PDF file
    selected_pdf = pdf_files[choice - 1]
    print(f"Processing '{selected_pdf}'...\n")
    
    # Convert the selected PDF to a txt file
    pdf_to_txt(selected_pdf)

# Run the main function
if __name__ == "__main__":
    main()
