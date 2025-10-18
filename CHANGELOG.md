# Changelog

Alle betydelige endringer i dette prosjektet vil bli dokumentert i denne filen.

Formatet er basert på [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
og dette prosjektet følger [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-27

### Added
- **Automatisk nettleser-deteksjon** - appen detekterer og velger automatisk tilgjengelige nettlesere
- **FFmpeg-validering** - sjekker om FFmpeg er tilgjengelig før nedlasting starter
- **Forbedret pyperclip-støtte** - valgfri avhengighet med elegant fallback til tkinter
- **Konfigurerbar filnavn-mal** - konstant for utdatafilnavn som kan enkelt endres

### Changed
- **pyperclip er nå valgfri** - appen fungerer uten pyperclip med fallback til tkinter's clipboard
- **Forbedret progress-visning** - forenklet logikk for element-labels
- **Bedre feilhåndtering** - mer robust håndtering av utklippstavle og avhengigheter
- **Oppdatert dokumentasjon** - README reflekterer nye funksjoner og valgfrie avhengigheter

### Fixed
- **Innstillingsvindu sentrering** - vinduet åpner nå midt på hovedvinduet
- **Visuell tilbakemelding ved avbrytelse** - knappen viser "Avbryter..." umiddelbart
- **Progress-logikk** - forenklet og mer lesbar kode for element-visning
- **Requirements.txt** - pyperclip markert som valgfri avhengighet

### Technical
- **Modulær arkitektur** - bedre separasjon av ansvar med dedikerte funksjoner
- **Konstant-definisjoner** - hardkodede verdier flyttet til konstanter
- **Forbedret feilhåndtering** - mer spesifikke exception-håndteringer
- **Kodekvalitet** - forenklet logikk og bedre lesbarhet

## [1.0.1] - 2025-10-18

### Added
- **Issue templates** for bug reports og feature requests
- **GitHub badges** for bedre presentasjon (Made with Python, Downloads)
- **Windows Defender advarsel** i README for usignert executable
- **Releases-seksjon** i README med nedlastingsinstruksjoner

### Changed
- **README struktur** med executable som anbefalt installasjonsmetode
- **Installasjonsveiledning** oppdatert med to metoder (executable vs. kildekode)
- **Badge-design** for bedre visuell appell

### Fixed
- **Repository-opprydding** - fjernet bygde artefakter fra Git
- **Gitignore-oppdatering** for å ekskludere build-filer

## [1.0.0] - 2025-10-18

### Added
- **Dark/Light mode toggle** i innstillinger med umiddelbar endring
- **Executable (.exe) versjon** av appen med PyInstaller
- **Distribusjonspakke** med alle nødvendige filer
- **Build-scripts** for å lage executable og distribusjon
- **GitHub-optimalisert README** med badges og strukturert informasjon
- **Requirements.txt** med alle avhengigheter
- **MIT-lisens** for åpen kildekode
- **Git-integrasjon** med .gitignore og versjonskontroll

### Changed
- **Mørk modus som standard** - appen starter nå med mørk tema
- **Forbedret innstillingssystem** med persistent lagring
- **Oppdatert brukerveiledning** med moderne Markdown-formatering

### Fixed
- **Dark mode-funksjonalitet** som var borte er nå gjenopprettet
- **Konfigurasjonshåndtering** for bedre brukeropplevelse
- **Temaendring** fungerer nå umiddelbart uten restart

### Technical
- **PyInstaller-konfigurasjon** for optimal executable-størrelse
- **Modularisert build-prosess** med separate scripts
- **Automatisert distribusjon** med timestamp-baserte filnavn
- **GitHub Actions-ready** struktur for CI/CD

## [0.1.0] - 2025-10-18

### Added
- **Grunnleggende nedlastingsfunksjonalitet** med yt-dlp
- **Grafisk brukergrensesnitt** med CustomTkinter
- **Støtte for flere formater** (MP4, MP3, original)
- **Kvalitetsvalg** (1080p, 720p, 480p, beste)
- **Cookie-integrasjon** fra nettlesere (Chrome, Edge, Firefox)
- **Spillelistehåndtering** med brukervalg
- **Drag & drop** for URLer
- **Progress tracking** med hastighet og ETA
- **Feilhåndtering** og robuste nedlastinger
- **Norsk språkstøtte** gjennom hele appen
- **Konfigurerbare innstillinger** med persistent lagring

### Technical
- **Threading-basert nedlasting** for responsiv GUI
- **FFmpeg-integrasjon** for mediebehandling
- **Moderne UI** med CustomTkinter dark theme
- **Robust feilhåndtering** med try/catch-struktur
- **JSON-basert konfigurasjon** for brukerinnstillinger

---

**Legende:**
- `Added` for nye funksjoner
- `Changed` for endringer i eksisterende funksjonalitet  
- `Deprecated` for snart utdaterte funksjoner
- `Removed` for fjernede funksjoner
- `Fixed` for feilrettinger
- `Security` for sikkerhetsrelaterte endringer
