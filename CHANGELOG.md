# Changelog

Alle betydelige endringer i dette prosjektet vil bli dokumentert i denne filen.

Formatet er basert på [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
og dette prosjektet følger [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
