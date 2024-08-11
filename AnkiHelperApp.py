import os

def display_menu(options):
    print("Please choose an option:")
    for option in options:
        print(option)
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def view_flashcards_template():
    file_path = 'anki_template.csv'
    if os.path.exists(file_path):
        print(f"Opening {file_path} in Excel...")
        os.system(f'start excel.exe "{file_path}"')
    else:
        print(f"Error: {file_path} not found in the current directory.")

def export_lectures_to_jpg():
    script_path = '2_pdf_to_jpg.py'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        os.system(f'python "{script_path}"')
    else:
        print(f"Error: {script_path} not found in the current directory.")

def add_personal_notes():
    script_path = '3_add_personal_notes.py'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        os.system(f'python "{script_path}"')
    else:
        print(f"Error: {script_path} not found in the current directory.")

def move_jpg_to_anki_folder():
    script_path = '4_move_jpg_to_anki_folder.py'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        os.system(f'python "{script_path}"')
    else:
        print(f"Error: {script_path} not found in the current directory.")

def main():
    print("This is app LECTURES-TO-ANKI")
    options = [
        "1| View Flashcards Template",
        "2| Export Lectures to JPG",
        "3| Add Personal Notes as HTML",
        "4| Move JPG to ANKI folder",
        "5| Exit and Close the App"
    ]

    while True:
        choice = display_menu(options)
        if choice == 5:
            print("Exiting and closing the app.")
            break
        elif choice == 1:
            view_flashcards_template()
        elif choice == 2:
            export_lectures_to_jpg()
        elif choice == 3:
            add_personal_notes()
        elif choice == 4:
            move_jpg_to_anki_folder()

if __name__ == "__main__":
    main()
