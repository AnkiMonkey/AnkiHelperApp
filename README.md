# CSV-to-ANKI + JPG-from-PDF
This pipeline provides a way to create complex flashcards in Excel (uploading to ANKI as .csv(utf8)) with appropriate cross-reference sources and jpg files created from lecture pdf file. 
It is based on ANKING's notetype addon (addon 952691989). 

Containing files:

**1) Excel template ** [CSV-to-ANKI.xlsl]
   Template for staying organized on a complex flashcards with a given lecture cross-reference, reference for added jpg, tag. 
   
**2) Python file** [JPG-from-PDF.py]
The python file creates ennumerated jpg files from de-cluttered pdf in the same folder as 'jpg_from_NAME-OF-PDF-FILE'.
Following this process:
lecture >> de-cluttered pdf >> enumerated jpg [JPG-from-PDF.py] >> Excel [CSV-to-ANKI.xlsl] >> ANKI (optimally FSRS mode - Q2/2024)

Columns as follows:
C1: Front
C2: Back
C3: Personal Notes >> reference to jpg needed as source in ANKI***, same format as C4
C4: Source >> V/P# S# (Vorlesung/Praktikum + Slide, e.g. V1 S2)
C5: Tag >> e.g. Subject::V1 indicating Vorlesung 1

*** to be added in ANKI w/ simple drag and drop


---
## Notes Q2/2024
-this system seems to be best of both worlds - providing  ANKING's notetype integrated to Excel deployable template

## TO-DO-LIST
-converting directly jpg as width=450, this 



