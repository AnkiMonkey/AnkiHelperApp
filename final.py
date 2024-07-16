import os
import subprocess

def main():
    print("This is app LECTURES-TO-ANKI")
    print("Please choose an option:")
    print("1| View Flashcards Template")
    print("2| Export Lectures to JPG")
    print("3| Add Personal Notes as HTML")
    print("4| Move JPG to ANKI folder)")   
    choice = input("Enter the number of your choice (1-4): ")

    if choice == '1':
        view_flashcards_template()
    elif choice == '2':
        export_lectures_to_jpg()
    elif choice == '3':
        add_personal_notes()
    elif choice == '4':
        move_jpg_to_anki_folder()
    else:
        print("Invalid choice. Please try again.")

def view_flashcards_template():
    file_path = 'anki_template.csv'
    if os.path.exists(file_path):
        print(f"Opening {file_path} in Excel...")
        subprocess.run(['start', 'excel.exe', file_path], shell=True)
    else:
        print(f"Error: {file_path} not found in the current directory.")

def export_lectures_to_jpg():
    script_path = '2_pdf_to_jpg.exe'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
    else:
        print(f"Error: {script_path} not found in the current directory.")

def add_personal_notes():
    script_path = '3_add_personal_notes.exe'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
    else:
        print(f"Error: {script_path} not found in the current directory.")

def move_jpg_to_anki_folder():
    script_path = '4_move_jpg_to_anki_folder.exe'
    if os.path.exists(script_path):
        print(f"Executing {script_path}...")
        subprocess.run([script_path], check=True)
    else:
        print(f"Error: {script_path} not found in the current directory.")

if __name__ == "__main__":
    main()
