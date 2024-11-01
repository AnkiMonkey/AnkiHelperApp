import os
from PyPDF2 import PdfReader, PdfWriter

def list_pdfs(folder_path):
    """Lists all PDF files in the specified folder and returns them as a list."""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    return pdf_files

def delete_page_from_pdf(pdf_path, page_to_delete):
    """
    Deletes a specific page from the specified PDF file.

    :param pdf_path: Path to the PDF file
    :param page_to_delete: Page number to delete (0-indexed)
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copy all pages except the one to delete
    for i in range(len(reader.pages)):
        if i != page_to_delete:
            writer.add_page(reader.pages[i])

    # Save the modified PDF with a new name
    new_pdf_path = f"{os.path.splitext(pdf_path)[0]}_modified.pdf"
    with open(new_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"Saved modified PDF as {new_pdf_path}")

def main():
    # Set the folder path (update as needed)
    folder_path = r"C:\Users\timon\Desktop\1 Uni\AnkiHelperApp"

    # List and display PDF files
    pdf_files = list_pdfs(folder_path)
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    print("Available PDF files:")
    for idx, pdf_file in enumerate(pdf_files):
        print(f"{idx + 1}: {pdf_file}")

    # Prompt user for file selection
    file_choice = int(input("Enter the number of the PDF file you want to modify: ")) - 1

    if file_choice < 0 or file_choice >= len(pdf_files):
        print("Invalid selection. Exiting.")
        return

    selected_pdf = os.path.join(folder_path, pdf_files[file_choice])
    print(f"Selected file: {pdf_files[file_choice]}")

    # Prompt user for the page to delete
    num_pages = len(PdfReader(selected_pdf).pages)
    print(f"This file has {num_pages} pages.")
    
    page_to_delete = int(input(f"Enter the page number to delete (1-{num_pages}): ")) - 1

    if page_to_delete < 0 or page_to_delete >= num_pages:
        print("Invalid page number. Exiting.")
        return

    # Delete the specified page from the selected PDF
    delete_page_from_pdf(selected_pdf, page_to_delete)

if __name__ == "__main__":
    main()
