# 📥 Nedlastarn - Brukerveiledning

> En moderne desktop-applikasjon for å laste ned videoer og lyd fra tusenvis av nettsteder med et elegant grafisk grensesnitt.

[![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://github.com)
[![Downloads](https://img.shields.io/github/downloads/mnytroe/Nedlastarn/latest/total.svg)](https://github.com/mnytroe/Nedlastarn/releases)

## 🚀 Installasjon

### Metode 1: Executable (Anbefalt)
1. **Last ned fra [Releases](https://github.com/mnytroe/Nedlastarn/releases)**
2. **Pakk ut ZIP-filen**
3. **Last ned FFmpeg** og legg `ffmpeg.exe` i samme mappe
4. **Kjør `Nedlastarn.exe`**

> ⚠️ **Windows Defender**: Kan advare om usignert executable. Dette er normalt - klikk "Mer info" → "Kjør likevel" eller legg til unntak.

### Metode 2: Fra kildekode
1. **Installer Python 3.8+** fra [python.org](https://python.org)
2. **Installer avhengigheter**:
   ```bash
   pip install yt-dlp customtkinter
   ```
   > **Valgfri**: `pip install pyperclip` for bedre utklippstavle-støtte
3. **Last ned FFmpeg** og legg `ffmpeg.exe` i samme mappe
4. **Kjør appen**:
   ```bash
   python Nedlastarn.py
   ```

## 📖 Grunnleggende bruk

### Steg 1: Lim inn URL
- Kopier URL-en til videoen du vil laste ned
- Lim den inn i tekstboksen øverst i programmet
- Du kan lime inn flere URLer (én per linje)

### Steg 2: Velg lagringsmappe
- Klikk **"Bla gjennom..."** for å velge hvor filen skal lagres
- Standard: Mappen "Nedlastinger" i hjemmemappen din

### Steg 3: Velg format og kvalitet
- **MP4 (video)**: For videoer - velg kvalitet (Beste/1080p/720p/480p)
- **MP3 (kun lyd)**: For bare lyd - velg bitrate (128/192/256/320 kbps)
- **Behold original**: Last ned i originalformat

### Steg 4: Start nedlasting
- Klikk **"Last ned"** for å starte
- Følg fremdriften i loggen nederst
- Klikk **"Avbryt"** hvis du vil stoppe

## ⚙️ Avanserte funksjoner

### 🍪 Cookies fra nettleser
Hvis en video krever innlogging:
- Programmet detekterer automatisk tilgjengelige nettlesere
- Velg nettleser (Chrome/Edge/Firefox) i dropdown-menyen
- Programmet bruker dine innloggede cookies automatisk

### 📜 Spillelister
Når du limer inn en spilleliste-URL:
- Programmet spør om du vil laste ned alle videoer eller bare den første
- Velg **"Alle"** for hele spillelisten
- Velg **"Kun første"** for bare første video

### 📁 Drag & Drop
- Dra URLer direkte fra nettleseren inn i tekstboksen
- Dra tekstfiler med URLer inn i programmet

## 🎨 Innstillinger

Klikk **"Innstillinger"** for å endre:

- ✅ Behold norske tegn i filnavn (æ/ø/å)
- ✅ Overskriv eksisterende filer
- ✅ Standard lagringsmappe
- 🌙 Dark/Light mode

## 💡 Spesielle tips

### NRK-videoer
- NRK-videoer lagres automatisk som **MKV** for best kvalitet
- Andre videoer lagres som **MP4**

### Filnavn
- Programmet fjerner automatisk ugyldige tegn fra filnavn
- Du kan velge å beholde norske tegn i innstillingene

### Feilsøking
- Hvis nedlasting feiler, sjekk at URL-en er gyldig
- For innloggede sider, prøv å velge riktig nettleser
- Programmet sjekker automatisk om FFmpeg er tilgjengelig før nedlasting starter
- Sørg for at FFmpeg er installert og tilgjengelig

## 🌐 Støttede nettsteder

Programmet støtter tusenvis av nettsteder, inkludert:

| Kategori | Eksempler |
|----------|----------|
| **Video** | YouTube, Vimeo, Dailymotion |
| **Norske** | NRK, TV2, VGTV |
| **Sosiale** | Twitter, Instagram, TikTok |
| **Streaming** | Twitch, Facebook Watch |

> Se [yt-dlp dokumentasjonen](https://github.com/yt-dlp/yt-dlp) for fullstendig liste.

## 🔧 Problemløsning

| Problem | Løsning |
|---------|---------|
| "FFmpeg ikke funnet" | Last ned ffmpeg.exe og legg den i samme mappe som programmet |
| "Mangler yt-dlp" | Kjør: `pip install yt-dlp` |
| Video krever innlogging | Velg riktig nettleser i dropdown-menyen |
| Programmet svarer ikke | Klikk "Avbryt" og prøv igjen |

## 🤝 Støtte og bidrag

Dette programmet bruker kraftige open source-verktøy:
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Nedlasting
- **[FFmpeg](https://ffmpeg.org/)** - Mediebehandling
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - GUI

For problemer med selve nedlastingen, sjekk [yt-dlp dokumentasjonen](https://github.com/yt-dlp/yt-dlp).

## ⚠️ Juridisk merknad

Dette verktøyet er kun ment for å laste ned innhold du har lovlig tilgang til. Respekter opphavsrett og nettstedenes vilkår for bruk.

---

**Laget med ❤️ i Norge**
