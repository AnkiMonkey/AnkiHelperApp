import PyPDF2
import os
import re

def list_pdfs_in_directory(directory):
    """List all PDF files in the given directory."""
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

def pdf_to_txt(pdf_file):
    """Convert a PDF file to a text file, omitting specific patterns."""
    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]
    txt_file = f"{pdf_name}.txt"
    
    # Define a pattern to omit lines like "Zoznam otázok z oblasti: LF - SUBJECT / #. strana"
    omit_pattern = re.compile(r"Zoznam otázok z oblasti: .+ / \d+\. strana")
    
    try:
        with open(pdf_file, 'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf)
            
            # Create or overwrite the text file
            with open(txt_file, 'w', encoding='utf-8') as txt:
                # Loop through each page and write text
                for page in reader.pages:
                    page_text = page.extract_text() or "[No extractable text]\n"
                    
                    # Filter out unwanted lines
                    filtered_text = "\n".join(
                        line for line in page_text.splitlines()
                        if not omit_pattern.match(line)
                    )
                    
                    # Write filtered text to file
                    txt.write(filtered_text + "\n")
        
        print(f"Text successfully written to {txt_file}")
        
        # Open the text file when done
        if os.name == 'nt':  # Windows
            os.startfile(txt_file)
        else:  # macOS/Linux
            os.system(f"open '{txt_file}'" if os.name == 'posix' else f"xdg-open '{txt_file}'")
    
    except Exception as e:
        print(f"Error processing {pdf_file}: {e}")

def main():
    """Main function to process PDFs in the current directory."""
    current_directory = os.getcwd()
    pdf_files = list_pdfs_in_directory(current_directory)
    
    if not pdf_files:
        print("No PDF files found in the current directory.")
        return
    
    print("Please choose a PDF to process:")
    for index, pdf in enumerate(pdf_files, start=1):
        print(f"{index}. {pdf}")
    
    while True:
        try:
            choice = int(input("Enter the number of the PDF you want to process: "))
            if 1 <= choice <= len(pdf_files):
                break
            print(f"Please choose a number between 1 and {len(pdf_files)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    selected_pdf = pdf_files[choice - 1]
    print(f"\nProcessing '{selected_pdf}'...\n")
    pdf_to_txt(selected_pdf)

if __name__ == "__main__":
    main()
