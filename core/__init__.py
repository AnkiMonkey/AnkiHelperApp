"""Spoločná logika pre AnkiHelperApp (GUI aj CLI).

Nič v tomto balíku nesmie volať input(), print() ani tkinter –
iba čisté funkcie, ktoré sa dajú testovať.
"""

APP_NAME = "AnkiHelperApp"
IMAGE_COLUMNS = ("Source", "Personal Notes", "Extra", "Missed Questions")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# Kvalita exportu – priorita je kvalita, veľkosť súborov je vedľajšia.
# 300 DPI = slajd 16:9 má ~4000 px na šírku (4K), ostré aj pri zoome.
# Viac (450/600) sa dá, ale obrázky 6000–8000 px môžu sekať v AnkiDroid/AnkiMobile.
LECTURE_DPI = 300
DOCUMENT_DPI = 300
# 100 + subsampling 0 (4:4:4) = prakticky bezstratové, farebný text sa nerozmazáva.
JPEG_QUALITY = 100
JPEG_SUBSAMPLING = 0

# Ochrana pred preklepom typu "1-9999" v bunke.
MAX_PAGES_PER_CELL = 50
