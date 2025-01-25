import os
import glob
import pandas as pd

# Define the folder path where the CSV files are located
folder_path = r'C:\Users\timon\Desktop\1B Uni-LF-PT\3 AnkiHelperApp'

# Get a list of all CSV files in the folder (and subdirectories if needed)
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Check if the list of files is correct
if not csv_files:
    print(f"No CSV files found in the folder: {folder_path}")
    exit()

# Enumerate the files and display them for user to choose
print(f"Found {len(csv_files)} CSV file(s):")
for idx, file in enumerate(csv_files, start=1):
    print(f"{idx}. {os.path.basename(file)}")

# Prompt the user to choose a CSV file from the list
file_choice = input(f"Enter the number of the CSV file you want to process (1-{len(csv_files)}): ")

# Validate the user input
if not file_choice.isdigit() or int(file_choice) < 1 or int(file_choice) > len(csv_files):
    print(f"Invalid choice. Please enter a number between 1 and {len(csv_files)}.")
    exit()

# Get the selected file
csv_file = csv_files[int(file_choice) - 1]
print(f"Processing file: {csv_file}")

# Prompt user to input PDF file name without extension
subject_name = input("Enter the abbreviation of the subject (without extension): ")

# Prompt user to specify if pages are from Vorlesung or Praktikum
print("Please choose the type of content:")
print("1. Vorlesung (Lecture)")
print("2. Praktikum (Practical)")
content_type_choice = input("Enter the number of your choice (1-2): ")

# Validate user input for content type
if content_type_choice not in ['1', '2']:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

# Determine if it's Vorlesung (V) or Praktikum (P)
content_type = 'V' if content_type_choice == '1' else 'P'

# Prompt user to input a number of Vorlesung or Praktikum
number_input = input(f"Enter the number of {content_type} (without extension as 01, 02... 10): ")

# Read the CSV into a pandas DataFrame with UTF-8 encoding
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    print(f"There was an encoding error reading the file {csv_file}. Please ensure the file is encoded in UTF-8.")
    exit()

# Function to update 'Missed Questions' and 'Personal Notes' columns with image HTML tag if numeric
def update_columns_with_image_tag(row):
    for column in ['Missed Questions', 'Personal Notes']:
        if column in row and pd.notna(row[column]):
            try:
                # Ensure the value is numeric
                value = int(row[column])
                image_tag = f'<img src="{subject_name}_{content_type}_{number_input}_S_{value:02d}.jpg" data-editor-shrink="false" width="450">'
                row[column] = image_tag
            except ValueError:
                pass  # Skip non-numeric values
    return row

# Apply the function row-wise to the DataFrame
df = df.apply(update_columns_with_image_tag, axis=1)

# Save the modified DataFrame back to the same CSV file with UTF-8 encoding
df.to_csv(csv_file, index=False, encoding='utf-8-sig')

# Display the first 100 rows of the modified DataFrame for verification
print("First 100 rows of the modified CSV:")
print(df.head(100))
