import os
from PyPDF2 import PdfReader, PdfWriter

def list_pdfs(folder_path):
    """Lists all PDF files in the specified folder and returns them as a list."""
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
    return pdf_files

def delete_pages_from_pdf(pdf_path, pages_to_delete):
    """
    Deletes specific pages from the specified PDF file.

    :param pdf_path: Path to the PDF file
    :param pages_to_delete: List of page numbers to delete (0-indexed)
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Copy all pages except the ones to delete
    for i in range(len(reader.pages)):
        if i not in pages_to_delete:
            writer.add_page(reader.pages[i])

    # Save the modified PDF with a new name
    new_pdf_path = f"{os.path.splitext(pdf_path)[0]}_modified.pdf"
    with open(new_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

    print(f"Saved modified PDF as {new_pdf_path}")

def parse_page_range(page_range, num_pages):
    """
    Parses a page range (e.g., '1-5') and returns a list of zero-indexed page numbers.

    :param page_range: A string representing the page range (e.g., '1-5')
    :param num_pages: The total number of pages in the PDF
    :return: A list of zero-indexed page numbers to delete
    """
    pages_to_delete = []

    # Check if it's a valid range
    try:
        if '-' in page_range:
            start, end = page_range.split('-')
            start, end = int(start.strip()) - 1, int(end.strip()) - 1

            if start < 0 or end >= num_pages or start > end:
                raise ValueError("Invalid page range.")

            # Generate the list of pages from start to end
            pages_to_delete = list(range(start, end + 1))
        else:
            # If it's just a single page number
            page_number = int(page_range.strip()) - 1
            if page_number < 0 or page_number >= num_pages:
                raise ValueError("Invalid page number.")
            pages_to_delete = [page_number]

    except ValueError as ve:
        print(f"Error parsing page range: {ve}")
        return []

    return pages_to_delete

def main():
    # Set the folder path (update as needed)
    folder_path = r"C:\Users\timon\Desktop\1B Uni-LF-PT\3 AnkiHelperApp"

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

    # Prompt user for the pages to delete
    num_pages = len(PdfReader(selected_pdf).pages)
    print(f"This file has {num_pages} pages.")
    
    # Ask the user to input a range of pages to delete (e.g., 1-5)
    page_range_input = input(f"Enter the page number or range to delete (1-{num_pages}), e.g., '1-5' or '3': ")

    # Parse the page range or single page
    pages_to_delete = parse_page_range(page_range_input, num_pages)
    
    if not pages_to_delete:
        return  # If parsing failed, stop execution
    
    # Delete the specified pages from the selected PDF
    delete_pages_from_pdf(selected_pdf, pages_to_delete)

if __name__ == "__main__":
    main()
