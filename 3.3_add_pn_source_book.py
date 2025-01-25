import os
import glob
import pandas as pd

# Define the folder path where the CSV files are located
folder_path = r'C:\Users\timon\Desktop\1B Uni-LF-PT\3 AnkiHelperApp'

# Get a list of all CSV files in the folder
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

# Set content type to BOOK
content_type_choice = "BOOK"

# Prompt user to input PDF file name without extension
book_name = input("Enter the abbreviation of the book: ")

# Read the CSV into a pandas DataFrame with UTF-8 encoding
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    print(f"There was an encoding error reading the file {csv_file}. Please ensure the file is encoded in UTF-8.")
    exit()

# Normalize column names to avoid issues with case or whitespace
df.columns = df.columns.str.strip()

# Check if the 'Personal Notes' column exists (formerly 'number')
if 'Personal Notes' not in df.columns:
    print("The column 'Personal Notes' does not exist in the selected file.")
    print("Available columns:", df.columns.tolist())
    exit()

# Check if the 'Source' column exists
if 'Source' not in df.columns:
    print("The column 'Source' does not exist in the selected file.")
    print("Available columns:", df.columns.tolist())
    exit()

# Function to modify the columns 'Personal Notes' and 'Source'
def update_column(row, column_name):
    value = row[column_name]
    if pd.notna(value):
        try:
            # Ensure the value is numeric
            formatted_value = f"{int(value):02d}" if int(value) < 100 else str(int(value))
            row[column_name] = f'<img src="{content_type_choice}_{book_name}_S_{formatted_value}.jpg" data-editor-shrink="false" width="450">'
        except ValueError:
            # Skip non-numeric values by leaving the row unchanged
            pass
    return row

# Apply the function to both 'Personal Notes' and 'Source' columns
df = df.apply(lambda row: update_column(row, 'Personal Notes'), axis=1)
df = df.apply(lambda row: update_column(row, 'Source'), axis=1)

# Save the modified DataFrame back to the same CSV file with UTF-8 encoding
df.to_csv(csv_file, index=False, encoding='utf-8-sig')

# Display the first 100 rows of the modified DataFrame for verification
print("First 100 rows of the modified CSV:")
print(df.head(100))
