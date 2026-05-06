<a id="readme-top"></a>

<h3 align="center">Správa prednášok pre ANKI</h3>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Obsah</summary>
  <ol>
    <li><a href="#about-the-project">O projekte</a></li>
    <ul>
      <li><a href="#prerequisites">Požiadavky</a></li>
    </ul>
    <li><a href="#usage">Použitie</a></li>
    <li><a href="#roadmap">Postup</a></li>
    <li><a href="#additional-notes">Ďalšie poznámky</a></li>
    <li><a href="#contact">Kontakt</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## O projekte

Tento nástroj je určený pre Slovákov a pomáha pripravovať materiály Cvičenie, Prednáška a Kniha z PDF/CSV súborov pre ANKI.

PDF/CSV v tej istej zložke aplikácie >> JPG obrázky / upravené CSV / TXT / upravené PDF >> ANKI

Aplikácia obsahuje funkcie na zjednodušenie nasledujúcich úloh:

- [1] Otvoriť priečinok s aplikáciou.
- [2] Exportovať PDF do JPG.
- [3] Pridať do CSV HTML značky pre obrázky.
- [4] Kopírovať alebo presunúť JPG súbory.
- [5] Extrahovať TXT z PDF.
- [6] Vymazať strany z PDF.
- [7] Premenovať PDF súbory.
- [8] Pridať tag do CSV.
- [9] Opraviť stĺpec Back pre import do ANKI.

### Riešenie

Tento pracovný tok je kombináciou viacerých nápadov a vylepšení:

- používanie ANKING notetype
- CSV ako vstup pre ANKI
- HTML odkazy na obrázky uložené v ANKI priečinku namiesto manuálneho kopírovania

### Vylepšenia

- Excel slúži ako manažér poznámok s prepojeniami medzi listami a odkazmi na prednášky v PDF.

<p align="center">
  <img src="./1.png" alt="Diagram" width="600"/>
</p>

- Každá téma môže mať vlastný list so vzájomným prepojením z hlavného listu, číslovaním a názvom. Tagy sa dajú filtrovať v jednom liste.

<p align="center">
  <img src="./2.png" alt="Diagram" width="600"/>
</p>

<p align="left">(<a href="#additional-notes">podrobnejšie informácie v časti Ďalšie poznámky</a>)</p>

<p align="left">(<a href="#readme-top">späť na začiatok</a>)</p>

<!-- GETTING STARTED -->
## Začíname
<p align="left">(<a href="#readme-top">späť na začiatok</a>)</p>

### Požiadavky
Excelová šablóna ANKI je vytvorená pre ANKING notetype. Ak používate základný typ (Basic), prispôsobte šablónu podľa seba.

<p align="left">(<a href="#readme-top">späť na začiatok</a>)</p>

<!-- USAGE EXAMPLES -->
## Použitie

### Python aplikácia
Spustite GUI aplikáciu *anki_gui.py* pomocou Pythonu.

Staršiu konzolovú aplikáciu *anki_app.exe* môžete ponechať vo zložke, ale aktívne rozhranie je v slovenčine.

Po spustení GUI si môžete vybrať jednu z nasledujúcich možností:

- [1] Otvoriť tento priečinok

      Otvorí priečinok, v ktorom je aplikácia. Vložte sem PDF a CSV súbory.

- [2] Exportovať PDF do JPG

      Konvertuje stránky PDF do JPEG obrázkov pre ANKI.

      Ak ide o materiál Cvičenie/Prednáška, aplikácia sa opýta na názov predmetu, typ a číslo.

      Súborové mená sa generujú podľa logiky:

      subject_name_C/P_##_S_##

      (C/P – Cvičenie/Prednáška; S – strana/slajd; ## – 01,02,10)

      Napr. O-CHEM1_C_01_S_02
      Napr. O-CHEM1_P_01_S_02

      Pre Knihu:

      KNIHA_nazovknihy_S_##

- [3] Pridať obrázkové tagy do CSV

      Spracuje CSV dáta a pridá HTML značky pre obrázky do vybraných stĺpcov.

      Podporované stĺpce: Source, Personal Notes, Extra, Missed Questions.

- [4] Kopírovať / presunúť JPG súbory

      Skopíruje alebo presunie exportované JPG súbory do cieľového priečinka.
      Pre ANKI vyberte priečinok collection.media.

- [5] Extrahovať TXT z PDF

      Extrahuje text z vybraného PDF do TXT súboru.

- [6] Vymazať strany z PDF

      Vytvorí nový upravený PDF súbor s odstránenými vybranými stranami.
      Príklad vstupu: 1,3,5-7

- [7] Premenovať PDF súbory

      Premenuje vybrané PDF súbory v priečinku aplikácie.

- [8] Pridať tag do CSV

      Pridá požadovaný tag do stĺpca Tags len tam, kde sú bunky prázdne.

- [9] Opraviť stĺpec Back

      Opraví formátovanie poľa Back pre ANKI HTML import.

### Excel

V Exceli môžete použiť tieto funkcie:

- [1] Hypertextové prepojenia na listy s prednáškami

  *=HYPERLINK("#'nazov_listu'!A1", "text_na_zobrazenie")*

  napr. *=HYPERLINK("#'P01'!A1", "Klikni pre Prednáška01")*

  Na presun medzi listami použite skratku *Ctrl + PgUp/PgDn*.

- [2] Hypertextové prepojenie na PDF prednášky

  *=HYPERLINK("cesta_k_pdf", "text_na_zobrazenie")*

  napr. *=HYPERLINK("C:\Users\User1\Desktop\ANKI\Lecture01.pdf", "Otvoriť Lecture01")*

<p align="left">(<a href="#roadmap">podrobnejšie kroky v časti Postup</a>)</p>

<p align="left">(<a href="#readme-top">späť na začiatok</a>)</p>

Zo šablóny treba exportovať iba list *3 ANKI ALL-LECTURES* do CSV (UTF-8). Všetky listy s ANKI poznámkami sa skopírujú sem.

(pre budúcnosť možno ako VBA makro, ktoré vyberie hodnoty zo všetkých listov okrem 1-3; problémom je však variabilita)

<!-- ROADMAP -->
## Postup
<a id="roadmap"></a>

1. **Pripravte vstupné súbory:**
   - Vložte PDF a CSV do rovnakého priečinka ako `anki_gui.py`.
   - Exportujte CSV súbory z Excelu do kódovania UTF-8.
   - Do CSV stĺpcov, ktoré majú byť obrázkovými tagmi, napíšte čísla strán.

2. **Spustite GUI:**
   - Spustite `anki_gui.py` pomocou Pythonu.
   - Použite slovenské tlačidlá v hlavnom okne.

3. **Výstup:**
   - Podľa výberu:
     - [1] Priečinok sa otvorí.
     - [2] PDF stránky sa exportujú do JPEG obrázkov.
     - [3] V CSV sa vytvoria obrázkové tagy.
     - [4] JPG súbory sa skopírujú alebo presunú do priečinka ANKI media.
     - [5] Z PDF sa extrahuje TXT.
     - [6] Vytvorí sa upravené PDF s odstránenými stranami.
     - [7] PDF súbory sa premenú.
     - [8] Do CSV sa pridajú tagy.
     - [9] Opraví sa formátovanie stĺpca Back.

<p align="left">(<a href="#readme-top">späť na začiatok</a>)</p>

<!-- ADDITIONAL NOTES -->
## Ďalšie poznámky
<a id="additional-notes"></a>

<p align="left">(<a href="#readme-top">späť na začiatok</a>)</p>

[1] Prispôsobiť CSV súbor pre HTML prepojenia:
- V Exceli v stĺpcoch Personal Notes a/alebo Source/Missed Questions pre cloze sa vložia:
  a) odkaz na JPEG
  b) width=450

Čísla strán pre Cvičenie/Prednáška/Kniha sa zapisujú ako 1,2,10,99,999 do stĺpcov Personal Notes a/alebo Source/Missed Questions.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Zdroje inšpirácie (kombinácia ANKING notetype a CSV vstupu s HTML odkazmi):

[1]  **The AnKing Note Types and Add-on** *https://www.youtube.com/watch?v=NYUhNMyAZNs*

[2]  **Importing Flashcards Into Anki** *https://www.youtube.com/watch?v=s0QQJp8HPd0*

[3] **Stop copying and pasting images into your flashcards** *https://www.youtube.com/watch?v=s0QQJp8HPd0*

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
<!-- CONTACT -->
## Kontakt

Pre otázky otvorte GitHub Issue v tomto repozitári.
