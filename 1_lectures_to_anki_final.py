import os

def main():
    while True:
        print("This is app LECTURES-TO-ANKI")
        print("Please choose an option:")
        print("1| View Flashcards Template")
        print("2| Export Lectures to JPG")
        print("3| Add Personal Notes as HTML")
        print("4| Move JPG to ANKI folder")
        print("5| Exit")
        
        choice = input("Enter the number of your choice (1-5): ")

        if choice == '1':
            view_flashcards_template()
        elif choice == '2':
            export_lectures_to_jpg()
        elif choice == '3':
            add_personal_notes()
        elif choice == '4':
            move_jpg_to_anki_folder()
        elif choice == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

def view_flashcards_template():
    file_path = 'anki_template.csv'
    if os.path.exists(file_path):
        print(f"Opening {file_path} in Excel...")
        os.system(f'start excel.exe "{file_path}"')
    else:
        print(f"Error: {file_path} not found in the current directory.")

def export_lectures_to_jpg():
    script_path = '2_pdf_to_jpg.exe'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        os.system(f'"{script_path}"')
    else:
        print(f"Error: {script_path} not found in the current directory.")

def add_personal_notes():
    script_path = '3_add_personal_notes.exe'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        os.system(f'"{script_path}"')
    else:
        print(f"Error: {script_path} not found in the current directory.")

def move_jpg_to_anki_folder():
    script_path = '4_move_jpg_to_anki_folder.exe'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        os.system(f'"{script_path}"')
    else:
        print(f"Error: {script_path} not found in the current directory.")

if __name__ == "__main__":
    main()
