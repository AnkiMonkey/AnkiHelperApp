import pandas as pd

# Define the input CSV file path
csv_file = 'Anki-personal-notes.csv'

# Read the CSV into a pandas DataFrame
df = pd.read_csv(csv_file)

# Function to check and add image HTMP tag if Personal Notes empty
def add_image_tag(row):
    # Example logic based on your description
    # Assuming column D contains the data as described
    image_tag = f'<img src="V_01-S_{row.name+1:02d}.jpg" data-editor-shrink="false" width="450">'
    if pd.isna(row['Source']):  # Check if cell in column D is empty
        row['Source'] = image_tag  # Add the image tag if empty
    return row

# Apply the function row-wise to the DataFrame
df = df.apply(add_image_tag, axis=1)

# Save the modified DataFrame back to CSV
df.to_csv('Anki-personal-notes_modified.csv', index=False)

# Display a sample of the modified CSV for verification
print("Sample of the modified CSV:")
print(df.head())  # Display the first few rows of the modified DataFrame
