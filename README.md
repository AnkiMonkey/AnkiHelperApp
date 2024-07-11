# CSV-to-ANKI + JPG-from-PDF
This pipeline provides a way to create complex flashcards in Excel [uploading to ANKI as .csv(utf8)] with appropriate cross-reference sources and jpg files created from lecture pdf file. 
It is based on ANKING's notetype addon (addon 952691989). 

Containing files:

**1) Excel template** [CSV-to-ANKI.xlsl]
   A template for staying organized on complex flashcards with a given lecture cross-reference, reference to add jpg, tag. 
   In trial (see **CSV-TO-ANKI_example_personal_notes_as_html_crosslink.csv**) Personal Notes + Sources as HTML crosslink to folder in which ANKI stores all pictures, following pipeline to be followed:
   [1] Copy paste pics needed to given folder
   [2] Adapt Personal Notes for given jpeg based on this snippet:
<
         img src="V_01-S_01.jpg" data-editor-shrink="false" width="450" 
         >
   
   -make sure that given jpeg is in the ANKI folder  (make sure to follow step [1])
   
   -the snippet also ensures width=450
   
   -due to complicated name, automatic ennumeration in Excel not possible, Python app       needed
   
   -ennumerated Personal Notes will appear, need to be adapted based on provided slides
   
   -to be seen in practice if Copy/Paste is not simplier on 09/24 
   [3] Run **add_personal_notes.py** 
   
**2) Python file** [JPG-from-PDF.py]
The python file creates ennumerated jpg files from de-cluttered pdf in the same folder as 'jpg_from_NAME-OF-PDF-FILE'.

Useful in following learning pipeline:

lecture >> de-cluttered pdf >> enumerated jpg [JPG-from-PDF.py] >> Excel [CSV-to-ANKI.xlsl] >> csv >> ANKI (optimally FSRS mode - Q2/2024)

Columns as follows:

C1: Front

C2: Back

C3: Personal Notes >> reference to jpg needed as source in ANKI (to be added in ANKI w/ simple drag and drop), same format as C4

C4: Source >> V/P# S# (Vorlesung/Praktikum + Slide, e.g. V1 S2)

C5: Tag >> e.g. Subject::V1 indicating Vorlesung 1

*** 

## Functionality
1) Tested on ANKI 24.06.2 Qt6
2) ANKING's notetype addon (addon 952691989) needed
3) Upon importing: 3a) separated by COMMA 3b) check each category if matches C1-C5
## Notes Q2/2024
-this system seems to be best of both worlds - providing  ANKING's notetype integrated to Excel deployable template

## TO-DO-LIST
-converting directly jpg as width=450 in app, upon trying, this resulted in blurry jpg in ANKI

-this bug persistent in other resizing add-ons 

-for now, resizing solved by doing manually in ANKI (adding htlm of Personal Notes with 'width=450')

-adding complex Excel fctions to work with internal data within sheets (e.g. VLOOKUP)

-adding dropdown lists w/ conditional formatting 
