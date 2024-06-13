# CSV-to-ANKI
This sample csv file provides a way to write cards in Excel (uploading to ANKI as .csv) 
It is based on ANKING's notetype. 
Containing files:
1) Excel template
   Template for staying organized on the flashcards with a given lecture cross-reference. 
2) Python file
The python file creates ennumerated jpg files from de-cluttered pdf in the same folder.
Following this pipeline:
lecture >> de-cluttered pdf >> enumerated jpg >> Excel (export as .csv) >> ANKI 

Columns as follows:
C1: Front
C2: Back
C3: Personal Notes >> reference to jpg needed as source in ANKI
C4: Source >> V/P# S# (Vorlesung/Praktikum + Slide, e.g. V1 S2)
C5: Tag >> e.g. Subject::V1 indicating Vorlesung 1

