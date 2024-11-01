import os

# Path to the main folder
main_folder = r"C:\Users\timon\Desktop\Uni"

# Function to get a list of folders in the main folder
def list_folders(directory):
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return folders

# Function to list all PDF files in the selected folder
def list_pdfs(directory):
    # Debugging print to show the directory being checked
    print(f"Checking for PDFs in: {directory}")
    
    # Full path must be used when checking file types
    pdfs = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.pdf')]
    
    # Debugging print to show what PDFs were found
    print(f"Found PDFs: {pdfs}")
    return pdfs

# Function to rename PDF files
def rename_pdf(directory, old_name, new_name):
    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name + ".pdf")  # Ensures .pdf is added
    os.rename(old_path, new_path)

# Main function
def main():
    # Step 1: List and enumerate all subfolders in the main folder
    folders = list_folders(main_folder)
    
    if not folders:
        print("No subfolders found.")
        return

    # Display subfolders to user with 0-based index
    print("Folders found:")
    for i, folder in enumerate(folders):
        print(f"{i}. {folder}")
    
    # Step 2: Ask the user to select a folder
    folder_choice = input(f"Select a folder (0-{len(folders)-1}): ")
    
    # Validate user input
    try:
        folder_choice = int(folder_choice)
        if folder_choice not in range(len(folders)):
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        return
    
    selected_folder = os.path.join(main_folder, folders[folder_choice])

    # Step 3: List all PDF files in the selected folder
    pdf_files = list_pdfs(selected_folder)
    
    if not pdf_files:
        print(f"No PDF files found in {selected_folder}.")
        return

    # Display PDF files with 0-based index
    print("PDF files found:")
    for i, pdf_file in enumerate(pdf_files):
        print(f"{i}. {pdf_file}")

    # Step 4: Ask the user which PDF to rename (with 0-based index)
    while True:
        file_choice = input(f"Select a PDF to rename (0-{len(pdf_files)-1}, or type 'e' to finish): ")

        if file_choice.lower() == "e":
            break
        
        # Validate the file choice
        try:
            file_choice = int(file_choice)
            if file_choice not in range(len(pdf_files)):
                raise ValueError
        except ValueError:
            print("Invalid choice. Please select a valid number or 'e' to quit.")
            continue

        # Step 5: Rename the selected PDF file
        selected_pdf = pdf_files[file_choice]
        new_name = input(f"Enter the new name for '{selected_pdf}' (do NOT add .pdf): ")

        # Rename the file
        rename_pdf(selected_folder, selected_pdf, new_name)
        print(f"Renamed '{selected_pdf}' to '{new_name}.pdf'")

        # Refresh the list of PDFs after renaming
        pdf_files = list_pdfs(selected_folder)
        print("Updated list of PDFs:")
        for i, pdf_file in enumerate(pdf_files):
            print(f"{i}. {pdf_file}")

if __name__ == "__main__":
    main()
