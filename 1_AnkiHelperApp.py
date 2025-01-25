import os

def main():
    while True:
        print("This is app AnkiHelperApp")
        print("Please choose an option:")
        print("1| View Flashcards Template")
        print("2| Export PDF to JPG (book/lecture)")
        print("3| Add Personal Notes + Source (basic/cloze/book)")
        print("4| Move JPG to ANKI folder")
        print("5| Extract TXT from PDF (book/lecture)")        
        print("6| Delete pages from PDF")
        print("7| Rename PDF Files")
        print("8| Add tag")
        print("9| Exit")
        
        choice = input("Enter the number of your choice (1-8): ")

        if choice == '1':
            view_flashcards_template()
        elif choice == '2':
            export_pdf_to_jpg()
        elif choice == '3':
            add_pn_source()
        elif choice == '4':
            move_jpg_to_anki_folder()
        elif choice == '5':
            extract_txt_from_pdf()
        elif choice == '6':
            delete_page_from_pdf()
        elif choice == '7':
            rename_pdf_files()
        elif choice == '8':
            add_tag()
        elif choice == '9':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

def view_flashcards_template():
    folder_path = r"C:\Users\timon\Desktop\1B Uni-LF-PT\3 AnkiHelperApp\templates"
    print(f"Opening flashcards template folder at: {folder_path}")
    os.startfile(folder_path)

def export_pdf_to_jpg():
    print("\n--- Export PDF to JPG ---")
    print("1. Export PDF to JPG (Lecture)")
    print("2. Export PDF to JPG (Book)")

    choice = input("Select an option (1-2): ")

    if choice == '1':
        run_script("2.1_pdf_to_jpg_lecture.py")
    elif choice == '2':
        run_script("2.2_pdf_to_jpg_book.py")
    else:
        print("Invalid choice. Returning to main menu.")

def add_pn_source():
    print("\n--- Add Personal Notes + Source ---")
    print("1. Add Personal Notes + Source (Basic)")
    print("2. Add Personal Notes + Source (Cloze)")
    print("3. Add Personal Notes + Source (Book)")

    choice = input("Select an option (1-3): ")

    if choice == '1':
        run_script("3.1_add_pn_source_basic.py")
    elif choice == '2':
        run_script("3.2_add_pn_source_cloze.py")
    elif choice == '3':
        run_script("3.3_add_pn_source_book.py")
    else:
        print("Invalid choice. Returning to main menu.")

def move_jpg_to_anki_folder():
    # Code to move JPG to the ANKI folder (for your specific implementation)
    run_script("4_move_jpg_to_anki_folder.py")

def extract_txt_from_pdf():
    print("\n--- Extract Text from PDF ---")
    print("1. Extract Text from PDF (Lecture)")
    print("2. Extract Text from PDF (Book)")

    choice = input("Select an option (1-2): ")

    if choice == '1':
        run_script("5.1_extract_txt_from_pdf_lecture.py")
    elif choice == '2':
        run_script("5.2_extract_txt_from_pdf_book.py")
    else:
        print("Invalid choice. Returning to main menu.")

def delete_page_from_pdf():
    # Code to delete pages from a PDF (for your specific implementation)
    run_script("6_delete_page_from_pdf.py")

def rename_pdf_files():
    # Code to rename PDF files (for your specific implementation)
    run_script("7_rename_pdf_files.py")

def add_tag():
    # Code to rename PDF files (for your specific implementation)
    run_script("8_add_tag_to_csv.py")

def run_script(script_name):
    try:
        if os.path.exists(script_name):
            os.system(f"python {script_name}")  # For Windows
        else:
            print(f"Error: {script_name} not found.")
    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")

if __name__ == "__main__":
    main()
