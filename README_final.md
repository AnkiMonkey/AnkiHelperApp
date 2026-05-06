<a id="readme-top"></a>

<h3 align="center">ANKI Lectures Management</h3>

<p align="center">
  <img src="main_window.png" width="400">
</p>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#getting-started">Getting Started</a></li>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
    </ul>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#additional-notes">Additional Notes</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

ANKI Lectures Management is a semi-automated tool designed to prepare Cvičenie, Prednáška, and Kniha materials from PDF/CSV files for ANKI.

PDF / CSV in the same app folder >> JPG images / edited CSV / TXT / modified PDF >> ANKI

The app includes functionalities to streamline the following tasks:

- [1] Otvoriť tento priečinok.
- [2] Exportovať PDF do JPG.
- [3] Pridať obrázkové tagy do CSV.
- [4] Kopírovať / presunúť JPG súbory.
- [5] Extrahovať TXT z PDF.
- [6] Vymazať strany z PDF.
- [7] Premenovať PDF súbory.
- [8] Pridať tag do CSV.
- [9] Opraviť stĺpec Back.

### Pipeline

The pipeline is an upgrated mix of following ideas with some tweeks:

- ANKING NOTETYPE
- CSV as input to ANKI
- HTML links of pictures located in ANKI Folder instead of copy/paste 

### Tweeks

- Excel to be used as general manager for notes with crosslinks in sheets and to lectures in pdf:

<p align="center">
  <img src="./1.png" alt="Diagram" width="600"/>
</p>

- Each topic on new sheet reachable from main sheet via crosslink, ennumerated and named, tags can be filtered within one sheet > notes for âˆ€ topic to be found here

<p align="center">
  <img src="./2.png" alt="Diagram" width="600"/>
</p>

<p align="left">(<a href="#additional-notes">for detailed references, Additional Notes</a>)</p>

<p align="left">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
<p align="left">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites
The Excel ANKI-Template is created for ANKING Notetype, otherwise adapt only for Basic type. 

<p align="left">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Python app
Launch the GUI app *anki_gui.py* with Python.

The older console app *anki_app.exe* can still be kept in the folder, but the active GUI interface is in Slovak.

After launching the GUI, you can choose from the following options:

- [1] Otvoriť tento priečinok

      Opens the folder where the app is located. Put PDFs and CSVs in this same folder.

- [2] Exportovať PDF do JPG

      Converts PDF pages to JPEG images for ANKI review.

      For Cvičenie/Prednáška material, the app asks for subject name, type, and number.

      Based on these logical names:

      subject_name_C/P_##_S_##

      (C/P - Cvičenie/Prednáška; S - Slide/Page; ## - 01,02,10)

      e.g. O-CHEM1_C_01_S_02
      e.g. O-CHEM1_P_01_S_02

      For Kniha material:

      KNIHA_bookname_S_##

- [3] Pridať obrázkové tagy do CSV

      Processes CSV data and adds ANKI HTML image tags to selected columns.

      Supported columns: Source, Personal Notes, Extra, Missed Questions.

- [4] Kopírovať / presunúť JPG súbory

      Copies or moves exported JPG files to a destination folder.
      For ANKI, choose the collection.media folder.

- [5] Extrahovať TXT z PDF

      Extracts text from a selected PDF into a TXT file.

- [6] Vymazať strany z PDF

      Creates a new modified PDF with selected pages removed.
      Example input: 1,3,5-7

- [7] Premenovať PDF súbory

      Renames selected PDF files in the app folder.

- [8] Pridať tag do CSV

      Adds the wished tag to the Tags column only where cells are empty.

- [9] Opraviť stĺpec Back

      Fixes Back field formatting for ANKI HTML import.

### Excel 

In Excel, following functions can be used: 

- [1] Hyperlinks to sheets with lectures
  
*=HYPERLINK("#'name_of_sheet'!A1", "text_to_see")*

e.g. *=HYPERLINK("#'P01'!A1", "Click to see Prednáška01")* 

Here keyboard shortcut *Ctrl + PgUp/PgDn* recommended for moving in sheets

- [2] Hyperlinks to pdf of lecture from location
- 
*=HYPERLINK("location_of_pdf", "text_to_see")*

e.g. *=HYPERLINK("C:\Users\User1\Desktop\ANKI\Lecture01.pdf", "Open Lecture01")*

<p align="left">(<a href="#roadmap">for detailed steps, see roadmap</a>)</p>

<p align="left">(<a href="#readme-top">back to top</a>)</p>

From the template, only sheet called *3 ANKI ALL-LECTURES* to be exported to csv (UTF-8), all sheets, i.e. ANKI notes, are to be copy/pasted here 

(for future, event. as VBA macro selecting all values in all sheets but 1-3; here is the challenge the variability though)

<!-- ROADMAP -->
## Roadmap
<a id="roadmap"></a>

1. **Prepare the Input Files:**
   - Put your PDF and CSV files in the same folder as `anki_gui.py`.
   - Export CSV files from Excel as UTF-8.
   - Put page numbers into the CSV columns that should become image tags.
   
2. **Run the GUI:**
   - Run `anki_gui.py` with Python.
   - Use the Slovak buttons in the main window.

3. **Output:**
   - Depending on your selection:
     - [1] Folder opened.
     - [2] PDF pages exported to JPEG images.
     - [3] CSV image tags created.
     - [4] JPG files copied or moved to the ANKI media folder.
     - [5] TXT extracted from PDF.
     - [6] Modified PDF created with selected pages deleted.
     - [7] PDF files renamed.
     - [8] Tags added to CSV.
     - [9] Back column formatting fixed.

<p align="left">(<a href="#readme-top">back to top</a>)</p>

<!-- ADDITIONAL NOTES -->
## Additional Notes
<a id="additional-notes"></a>

<p align="left">(<a href="#readme-top">back to top</a>)</p>

[1] Adapt the CSV File for HTML Crosslinks:
- In Excel Personal Notes and/or Source/Missed Questions (for cloze) transformation will specifie both:
  a) Jpeg crosslink
  b) width=450

The Cvičenie/Prednáška/Kniha page number is to be written as 1,2,10,99,999 to columns under Personal Notes and/or Source/Missed Questions.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Sources for the idea (mixed ANKING notetype + input as CSV w/ HTML links):

[1]  **The AnKing Note Types and Add-on** *https://www.youtube.com/watch?v=NYUhNMyAZNs*

[2]  **Importing Flashcards Into Anki** *[[https://www.youtube.com/watch?v=s0QQJp8HPd0](https://www.youtube.com/watch?v=s0QQJp8HPd0)](https://www.youtube.com/watch?v=DIkynwCHLfA)*

[3] **Stop copying and pasting images into your flashcards** *https://www.youtube.com/watch?v=s0QQJp8HPd0*

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
<!-- CONTACT -->
## Contact

Timon Nemeth - timon.nemeth@gmail.com

Project Link: [https://github.com/AnkiMonkey/ANKI-Lectures-Management](https://github.com/AnkiMonkey/AnkiHelperApp)

