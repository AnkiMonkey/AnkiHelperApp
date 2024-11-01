import os
import shutil

def copy_or_move_files():
    # Prompt the user for the source folder name
    source_folder = input("Enter the name of the folder to copy/move files from: ")

    # Check if the folder exists
    if not os.path.isdir(source_folder):
        print(f"The folder '{source_folder}' does not exist.")
        return

    # Specify the fixed destination path
    destination_path = r"C:\Users\timon\AppData\Roaming\Anki2\User 1\collection.media"
    # Create the destination folder if it does not exist
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Prompt the user for the action (copy or move)
    print("Choose an option:")
    print("1. Copy files")
    print("2. Move files")
    action = input("Enter 1 or 2: ")

    # List the files in the source folder
    files = os.listdir(source_folder)

    # Perform the selected action
    if action == '1':
        for file in files:
            source_file = os.path.join(source_folder, file)
            if os.path.isfile(source_file):  # Make sure it's a file, not a folder
                shutil.copy(source_file, destination_path)
                print(f"Copied file: {file}")
        print("File copy completed.")
    elif action == '2':
        for file in files:
            source_file = os.path.join(source_folder, file)
            if os.path.isfile(source_file):  # Make sure it's a file, not a folder
                shutil.move(source_file, destination_path)
                print(f"Moved file: {file}")
        print("File move completed.")
    else:
        print("Invalid option. Please enter 1 or 2.")

if __name__ == "__main__":
    copy_or_move_files()
