import os
import pandas as pd

def list_csv_files(folder_path):
    """List all CSV files in the folder and return a list of filenames."""
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    return files

def process_selected_files(folder_path, selected_files, new_tag_value):
    """Process the selected CSV files and modify the 'Tags' column only if it's empty."""
    for filename in selected_files:
        file_path = os.path.join(folder_path, filename)
        try:
            # Open CSV with utf-8 encoding
            df = pd.read_csv(file_path, encoding='utf-8')
            if 'Tags' in df.columns:
                # Only update 'Tags' column where the value is missing (NaN or empty)
                df['Tags'] = df['Tags'].fillna(new_tag_value)
                # Save the file with utf-8 encoding and ensure Excel compatibility (BOM)
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"Updated 'Tags' column in {filename}")
            else:
                print(f"Column 'Tags' not found in {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

def main():
    """Main function to execute the script."""
    folder_path = r"C:\Users\timon\Desktop\1B Uni-LF-PT\3 AnkiHelperApp"  # Default folder path
    print("Listing all CSV files in the folder:")
    
    files = list_csv_files(folder_path)
    if not files:
        print("No CSV files found in the folder.")
        return

    # Let the user select which files to process
    selected_indices = input("Enter the numbers of the files you want to process (separate with commas): ")
    selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(',') if i.strip().isdigit()]

    selected_files = [files[i] for i in selected_indices if 0 <= i < len(files)]
    
    if not selected_files:
        print("No valid files selected. Exiting.")
        return

    new_tag_value = input("Enter the value you want to set for the 'Tags' column (only where empty): ")
    process_selected_files(folder_path, selected_files, new_tag_value)
    print("Finished processing the selected CSV files.")

if __name__ == "__main__":
    main()
