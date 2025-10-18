========================================
           NEDLASTARN - BRUKERVEILEDNING
========================================


Nedlastarn er et grafisk program for å laste ned videoer og lyd fra
tusenvis av nettsteder som YouTube, NRK, Vimeo og mange flere.


========================================
            INSTALLASJON
========================================


1. Sørg for at du har Python installert på datamaskinen din
   (Last ned fra: https://python.org)


2. Installer nødvendige avhengigheter ved å åpne kommandolinjen
   og skrive:
   
   pip install yt-dlp customtkinter pyperclip


3. Last ned FFmpeg og legg ffmpeg.exe i samme mappe som nedlastarn.py
   (Last ned fra: https://ffmpeg.org/download.html)


4. Kjør programmet ved å dobbeltklikke på nedlastarn.py


========================================
            GRUNNLEGGENDE BRUK
========================================


STEG 1: Lim inn URL
------------------
• Kopier URL-en til videoen du vil laste ned
• Lim den inn i tekstboksen øverst i programmet
• Du kan lime inn flere URLer (én per linje)


STEG 2: Velg lagringsmappe
--------------------------
• Klikk "Bla gjennom..." for å velge hvor filen skal lagres
• Standard: Mappen "Nedlastinger" i hjemmemappen din


STEG 3: Velg format og kvalitet
-------------------------------
• MP4 (video): For videoer - velg kvalitet (Beste/1080p/720p/480p)
• MP3 (kun lyd): For bare lyd - velg bitrate (128/192/256/320 kbps)
• Behold original: Last ned i originalformat


STEG 4: Start nedlasting
------------------------
• Klikk "Last ned" for å starte
• Følg fremdriften i loggen nederst
• Klikk "Avbryt" hvis du vil stoppe


========================================
            AVANSERTE FUNKSJONER
========================================


COOKIES FRA NETTLESER
---------------------
Hvis en video krever innlogging:
• Velg nettleser (Chrome/Edge/Firefox) i dropdown-menyen
• Programmet bruker dine innloggede cookies automatisk


SPILLELISTER
------------
Når du limer inn en spilleliste-URL:
• Programmet spør om du vil laste ned alle videoer eller bare den første
• Velg "Alle" for hele spillelisten
• Velg "Kun første" for bare første video


DRAG & DROP
-----------
• Dra URLer direkte fra nettleseren inn i tekstboksen
• Dra tekstfiler med URLer inn i programmet


========================================
            INNSTILLINGER
========================================


Klikk "Innstillinger" for å endre:


• Behold norske tegn i filnavn (æ/ø/å)
• Overskriv eksisterende filer
• Standard lagringsmappe


========================================
            SPESIELLE TIPS
========================================


NRK-VIDEOER
-----------
• NRK-videoer lagres automatisk som MKV for best kvalitet
• Andre videoer lagres som MP4


FILNAVN
-------
• Programmet fjerner automatisk ugyldige tegn fra filnavn
• Du kan velge å beholde norske tegn i innstillingene


FEILSØKING
----------
• Hvis nedlasting feiler, sjekk at URL-en er gyldig
• For innloggede sider, prøv å velge riktig nettleser
• Sørg for at FFmpeg er installert og tilgjengelig


========================================
            STØTTEDE NETTSTEDER
========================================


Programmet støtter tusenvis av nettsteder, inkludert:
• YouTube, Vimeo, Dailymotion
• NRK, TV2, VGTV
• Twitter, Instagram, TikTok
• Og mange flere!


Se yt-dlp dokumentasjonen for fullstendig liste.


========================================
            PROBLEMLØSNING
========================================


PROBLEM: "FFmpeg ikke funnet"
LØSNING: Last ned ffmpeg.exe og legg den i samme mappe som programmet


PROBLEM: "Mangler yt-dlp"
LØSNING: Kjør: pip install yt-dlp


PROBLEM: Video krever innlogging
LØSNING: Velg riktig nettleser i dropdown-menyen


PROBLEM: Programmet svarer ikke
LØSNING: Klikk "Avbryt" og prøv igjen


========================================
            KONTAKT OG STØTTE
========================================


Dette programmet bruker yt-dlp og FFmpeg.
• yt-dlp: https://github.com/yt-dlp/yt-dlp
• FFmpeg: https://ffmpeg.org


For problemer med selve nedlastingen, sjekk yt-dlp dokumentasjonen.


========================================





