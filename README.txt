NEW ANKI HELPER

How to use:

1. Put your PDF and CSV files in this same new_anki folder.
2. Double-click anki_app.exe.
3. Choose what you want to do from the menu.

GUI version:

There is also a graphical version:

anki_gui.py

Run it with Python if you want buttons instead of the console menu.

The app works only with files in this same folder. It does not use hidden hardcoded folders.

Menu options:

1. Export PDF to JPG
   Converts PDF pages into JPG images.

2. Add image tags to CSV
   Replaces page numbers in supported columns with Anki image HTML.
   Supported columns:
   Source
   Personal Notes
   Extra
   Missed Questions

3. Copy/move JPG files
   Copies or moves image files from a folder into a destination folder.
   For Anki, choose your Anki collection.media folder as the destination.

4. Extract text from PDF
   Creates a TXT file from a PDF.

5. Delete PDF pages
   Creates a new modified PDF with selected pages removed.
   Example input:
   1
   1,3,5
   1-5
   1,3,5-7

6. Rename PDF
   Renames a PDF in this folder.

7. Add tag to CSV
   Adds a tag only where the Tags column is empty.

8. Fix Back column
   Fixes Back field formatting for Anki HTML import.

Important:

The app usually creates new output files instead of overwriting originals.

Examples:

original.csv -> original_images.csv
original.csv -> original_tagged.csv
original.csv -> original_fixed.csv
lecture.pdf -> lecture_modified.pdf

When importing CSV files into Anki, enable HTML in fields if the CSV contains image tags or formatted Back fields.
