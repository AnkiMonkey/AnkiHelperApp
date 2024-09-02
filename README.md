<a id="readme-top"></a>

<h3 align="center">ANKI Lectures Management</h3>

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
    <li><a href="#roadmap">ADDITIONAL NOTES</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

ANKI Lectures Management is a semi-automated tool designed to automate the management of exporting lecture materials and notes from lectures (as pdf) to ANKI as follows:

LECTURE (pdf) >> Flashcards in Excel (csv), JPG from PDF >> ANKI 

The app includes functionalities to streamline the following tasks:

- [1] Opening an Excel-template for creating flashcards.
- [2] Exporting lecture slides to JPG to be used on flashcards.
- [3] Semi-automating the process of adding personal notes as HTML crosslink.
- [4] Moving exported JPG files to the ANKI pictures directory (being cross-linked as HTML).

### Pipeline

The pipeline is an upgrated mix of following ideas with some tweeks:

- ANKING NOTETYPE
- CSV as input to ANKI
- HTML links instead of copy/paste of pictures

### Tweeks
- Excel to be used as general manager for notes with 
- 

For links see

<p align="left">(<a href="#ADDITIONAL NOTES">see ADDITIONAL NOTES</a>)</p>

<p align="left">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
<p align="left">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites
Ensure you have Python installed. Additionally, the following Python libraries are required:

- pandas
- openpyxl
- matplotlib
- fitz
- PIL

Ensure you have ANKI installed (V. 24.06.3 Qt6 or above)
The Excel ANKI-Template is created for ANKING Notetype

<p align="left">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Python app
Launch app *AnkiHelperApp*

Upon launching the app, you can choose from the following options:

- [1] View Flashcards Template (anki_template.csv)
      Opens the ANKI flashcards template in Excel for viewing and editing.
      
- [2] Export Lectures to JPG (pdf_to_jpg.py)
      Converts lecture slides from a PDF file to JPEG images for ANKI review. The user is promted to write a name and number of Vorlesung/Praktikum 
      -based on these logical names: 
      subject_name_V/P_##_S_##
      (V/P - Vorlesung/Praktikum; S - Slide; ## - 01,02,10)
      e.g. O-CHEM1_V_01_S02
      
- [3] Add Personal Notes as HTML (add_personal_notes.py)
      Processes ANKI template data to add HTML image tags when 'Source' information is missing.
      
- [4] Move Exported JPG to ANKI Pictures Directory and Link as HTML
      Moves the exported JPG files to the ANKI pictures directory and creates HTML links for ANKI cards.

### Excel 
In Excel, following functions can be used: 

- [1] Hyperlinks to sheets with lectures
- 
*=HYPERLINK("#'name_of_sheet'!A1", "text_to_see")*

e.g. *=HYPERLINK("#'V01'!A1", "Click to see Vorlesung01")* 

Here keyboard shortcut Ctrl + PgUp/PgDn recommended for moving in sheets

- [2] Hyperlinks to pdf of lecture from location
- 
*=HYPERLINK("location_of_pdf", "text_to_see")*

e.g. *=HYPERLINK("C:\Users\User1\Desktop\ANKI\Lecture01.pdf", "Open Lecture01")*

<p align="left">(<a href="#roadmap">for detailed steps, see roadmap</a>)</p>

<p align="left">(<a href="#readme-top">back to top</a>)</p>

From the template, only sheet called *3 ANKI ALL-LECTURES* to be exported to csv (UTF-8), all sheets are to be copy/pasted here 

(for future, event. as VBA macro selecting all values in all sheets but 1-3; here is the challenge the variability though)

<!-- ROADMAP -->
## Roadmap
<a id="roadmap"></a>

1. **Prepare the Input CSV File:**
   - Ensure your ANKI template file is named `anki_template.csv`.
   - Place `anki_template.csv` in the same directory as the script.
   - Manually edit `anki_template.csv` as needed.
   
2. **Run the Script:**
   - Execute the chosen script based on your needs.

3. **Output:**
   - Depending on your selection:
     - [1] ANKI flashcards template viewed and edited in Excel.
     - [2] Lecture slides exported to JPEG images.
     - [3] Personal notes added to ANKI cards in HTML format.
     - [4] JPG files moved to the ANKI pictures directory and linked as HTML for ANKI cards.

<p align="left">(<a href="#readme-top">back to top</a>)</p>

<!-- ADDITIONAL NOTES -->
## Additional Notes
<p align="left">(<a href="#readme-top">back to top</a>)</p>

[1] Add JPEGs to ANKI Pictures Folder:
- Move the exported JPEG files to the ANKI pictures directory where they are stored. This folder path is also pinned by Quick access:
  Paste to this folder (path): `C:\Users\timon\AppData\Roaming\Anki2\1. Timon - Pharmazeutische Fakultät\collection.media`

[2] Adapt the CSV File for HTML Crosslinks:
- In the ANKI Personal Notes specified both:
  a) Jpeg crosslink
  b) width=450
- Run `add_personal_notes.py` to automate the HTML crosslink generation using Python (pandas library).

Sources for the idea (mixed ANKING notetype + input as CSV w/ HTML links):
[1]  
[https://www.youtube.com/watch?v=s0QQJp8HPd0](https://www.youtube.com/watch?v=s0QQJp8HPd0)

<!-- CONTACT -->
## Contact

Timon Nemeth - timon.nemeth@gmail.com

Project Link: [https://github.com/AnkiMonkey/ANKI-Lectures-Management](https://github.com/AnkiMonkey/ANKI-Lectures-Management)

---

# LECTURES-TO-ANKI

This section provides tools and scripts to manage lecture materials and notes for ANKI, enhancing study efficiency.

## Options:

1. **View Flashcards Template (anki_template.csv)**
   - Opens the ANKI flashcards template in Excel for viewing and editing.

2. **Export Lectures to JPG (pdf_to_jpg.py)**
   - Converts lecture slides from a PDF file to JPEG images for ANKI review.

3. **Add Personal Notes as HTML (add_personal_notes.py)**
   - Processes ANKI template data to add HTML image tags when 'Source' information is missing.

4. **Move Exported JPG to ANKI Pictures Directory and Link as HTML**
   - Moves the exported JPG files to the ANKI pictures directory and creates HTML links for ANKI cards.

## Instructions:

### Getting Started
Ensure Python and required libraries are installed. Review prerequisites for detailed requirements.

### Usage
Choose an option by entering the respective number and follow the prompts.

### Example Workflow:
- **For Option 1:** Ensure `anki_template.csv` exists in the current directory. Opens this file in Excel for viewing and editing ANKI flashcards.
- **For Option 2:** Ensure `pdf_to_jpg.py` is available. Converts lecture slides from a specified PDF file to JPEG images for ANKI.
- **For Option 3:** Ensure `add_personal_notes.py` is accessible. Adds HTML image tags to ANKI cards based on predefined rules.
- **For Option 4:** Ensures JPG files are moved to the ANKI pictures directory and linked as HTML for ANKI cards.

### Contact
Timon Nemeth - timon.nemeth@gmail.com
