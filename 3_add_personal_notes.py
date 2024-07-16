import pandas as pd

# Define the input CSV file path
csv_file = 'anki_template.csv'

# Prompt user to input PDF file name without extension
subject_name = input("Enter the abbreviation of the subject (without extension): ")

# Prompt user to specify if pages are from Vorlesung or Praktikum
print("Please choose the type of content:")
print("1. Vorlesung (Lecture)")
print("2. Praktikum (Practical)")
content_type_choice = input("Enter the number of your choice: ")

# Validate user input for content type
if content_type_choice not in ['1', '2']:
    print("Invalid choice. Please enter 1 or 2.")
    exit()

# Determine if it's Vorlesung (V) or Praktikum (P)
if content_type_choice == '1':
    content_type = 'V'
elif content_type_choice == '2':
    content_type = 'P'

# Prompt user to input a number of Vorlesung or Praktikum
number_input = input(f"Enter the number of {content_type} (without extension as 01, 02... 10): ")
# Read the CSV into a pandas DataFrame with UTF-8 encoding
try:
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    print("There was an encoding error reading the file. Please ensure the file is encoded in UTF-8.")
    exit()

# Function to check and add image HTML tag if 'Source' column is empty
def add_image_tag(row):
    image_tag = f'<img src="{subject_name}_{content_type}_{number_input}_S_{row.name+1:02d}.jpg" data-editor-shrink="false" width="450">'
    print(image_tag)
    if pd.isna(row['Source']):  # Check if cell in column 'Source' is empty
        row['Source'] = image_tag  # Add the image tag if empty
    return row

# Apply the function row-wise to the DataFrame
df = df.apply(add_image_tag, axis=1)

# Save the modified DataFrame back to the same CSV file with UTF-8 encoding
df.to_csv(csv_file, index=False, encoding='utf-8-sig')

# Display the first 100 rows of the modified DataFrame for verification
print("First 100 rows of the modified CSV:")
print(df.head(100))  # Display the first 100 rows of the modified DataFrame
