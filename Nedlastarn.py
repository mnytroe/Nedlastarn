import os
import sys
import json
import threading
import queue
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk


# Avhengigheter:
# pip install yt-dlp customtkinter pyperclip (pyperclip er valgfri)
try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError, DownloadCancelled
except Exception as e:
    raise SystemExit(
        "Mangler 'yt_dlp'. Installer med: pip install yt-dlp\nFeil: " + str(e)
    )

# Valgfri avhengighet for utklippstavle
HAS_PYPERCLIP = False
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    pass


APP_NAME = "Nedlastarn"
CONFIG_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / APP_NAME
CONFIG_PATH = CONFIG_DIR / "config.json"

# Konstanter for filnavn-maler
DEFAULT_OUTPUT_TEMPLATE = "%(title)s [%(id)s].%(ext)s"
SIMPLE_OUTPUT_TEMPLATE = "%(title)s.%(ext)s"




def ensure_ffmpeg_on_path():
    app_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    candidates = [
        app_dir / "ffmpeg.exe",
        Path.cwd() / "ffmpeg.exe",
        Path(os.environ.get("PROGRAMFILES", "")) / "ffmpeg/bin/ffmpeg.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "ffmpeg/bin/ffmpeg.exe",
    ]
    if shutil.which("ffmpeg"):
        return
    for exe in candidates:
        if exe and exe.exists():
            os.environ["PATH"] = str(exe.parent) + os.pathsep + os.environ.get("PATH", "")
            break


ensure_ffmpeg_on_path()


BROWSER_CANDIDATES = {
    "chrome": [
        Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
        Path.home() / "AppData/Local/Google/Chrome/Application/chrome.exe",
    ],
    "edge": [
        Path(os.environ.get("PROGRAMFILES", "")) / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Microsoft/Edge/Application/msedge.exe",
        Path.home() / "AppData/Local/Microsoft/Edge/Application/msedge.exe",
    ],
    "firefox": [
        Path(os.environ.get("PROGRAMFILES", "")) / "Mozilla Firefox/firefox.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Mozilla Firefox/firefox.exe",
        Path.home() / "AppData/Local/Mozilla Firefox/firefox.exe",
    ],
}


def _check_ffmpeg() -> bool:
    """Sjekk om FFmpeg er tilgjengelig"""
    return shutil.which("ffmpeg") is not None


def autodetect_browser() -> str:
    for key, paths in BROWSER_CANDIDATES.items():
        for p in paths:
            if p and p.exists():
                return key
    return "none"


DEFAULT_CONFIG = {
    "keep_norwegian_chars": False,
    "default_dir": str(Path.home() / "Nedlastinger"),
    "overwrite_existing": False,
    "dark_mode": True,
}


def load_config() -> dict:
    try:
        if CONFIG_PATH.exists():
            return {**DEFAULT_CONFIG, **json.loads(CONFIG_PATH.read_text(encoding="utf-8"))}
    # Din forbedrede feilhåndtering:
    except (json.JSONDecodeError, PermissionError) as e:
        print(f"Advarsel: Kunne ikke laste konfigurasjonsfilen ({CONFIG_PATH}). Bruker standardinnstillinger. Feil: {e}")
    except Exception as e:
        # En generell fallback for andre uventede feil
        print(f"Advarsel: En uventet feil oppstod ved lasting av config. Bruker standardinnstillinger. Feil: {e}")
   
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print("Kunne ikke lagre config:", e)


class Downloader(threading.Thread):
    def __init__(self, urls: list[str], out_dir: Path, mode: str, quality: str,
                 browser: str, keep_norwegian: bool, overwrites: bool, msgs: queue.Queue,
                 mp3_quality: str = "192", playlist_items: str | None = None):
        super().__init__(daemon=True)
        self.urls = urls
        self.out_dir = out_dir
        self.mode = mode
        self.quality = quality
        self.browser = browser
        self.keep_norwegian = keep_norwegian
        self.overwrites = overwrites
        self.msgs = msgs
        self.mp3_quality = mp3_quality
        self.playlist_items = playlist_items
        self._cancel = False
        self._last_filename = None
        self._last_pl_index = None
        self._pl_decision_q: queue.Queue[str] = queue.Queue()


    def log(self, text: str):
        self.msgs.put(("log", text))


    def prog(self, pct: float | None, speed_bps: float | None, eta_s: int | None, filename: str | None = None, item_info: dict | None = None):
        self.msgs.put(("progress", pct, speed_bps, eta_s, filename, item_info))


    def _request_playlist_decision(self, approx_total):
        self.msgs.put(("ask_playlist", approx_total))


    def set_playlist_decision(self, choice: str):
        self._pl_decision_q.put(choice)


    def progress_hook(self, d):
        if self._cancel:
            raise DownloadCancelled("User cancelled")
        status = d.get("status")
        info = d.get("info_dict", {}) or {}
        fname = d.get("filename") or info.get("_filename")
        if fname:
            self._last_filename = fname
        pl_index = info.get("playlist_index")
        n_entries = info.get("n_entries") or info.get("playlist_count")
        if pl_index and pl_index != self._last_pl_index:
            self._last_pl_index = pl_index
            total = int(n_entries) if n_entries else "?"
            self.log(f"  Spilleliste-element: {pl_index} av {total}")
        item_info = {"i": None, "n": None, "title": info.get("title")}
        try:
            if pl_index: item_info["i"] = int(pl_index)
            if n_entries: item_info["n"] = int(n_entries)
        except Exception: pass
        if status == "downloading":
            p = d.get("downloaded_bytes", 0)
            t = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            pct = (p / t * 100) if t else 0
            spd = d.get("speed")
            eta = d.get("eta")
            if item_info.get("i") and item_info.get("n"):
                overall_pct = ((item_info["i"] - 1) + (pct / 100.0)) / item_info["n"] * 100.0
            else:
                overall_pct = pct
            self.prog(overall_pct, spd, eta, fname, item_info)
        elif status == "finished":
            self.log("  Ferdig nedlastet. Konverterer (ffmpeg)…")
            self.prog(100.0, None, None, fname, item_info)


    def _fmt_for_quality(self):
        hmax = {"1080p": 1080, "720p": 720, "480p": 480}.get(self.quality)
        if self.mode == "mp3": return "bestaudio/best"
        if hmax: return f"bv*[height<={hmax}]+ba/best[height<={hmax}]"
        return "bv*+ba/best"


    def run(self):
        try:
            self.out_dir.mkdir(parents=True, exist_ok=True)
            base_opts = {
                "outtmpl": str(self.out_dir / DEFAULT_OUTPUT_TEMPLATE),
                "progress_hooks": [self.progress_hook], "noprogress": True, "nopart": True,
                "concurrent_fragment_downloads": 5, "retries": 5, "fragment_retries": 5,
                "socket_timeout": 20, "overwrites": self.overwrites,
                "restrictfilenames": not self.keep_norwegian, "windowsfilenames": True,
                "trim_file_name": 200, "download_archive": str(self.out_dir / "downloaded.txt"),
                "quiet": True, "no_warnings": True, "extractor_args": {"youtube": {"skip": ["translated_subs"]}},
                "postprocessor_hooks": [lambda d: (_ for _ in ()).throw(DownloadCancelled("User cancelled")) if self._cancel else None],
            }
            fmt = self._fmt_for_quality()
            for url in self.urls:
                if self._cancel: raise DownloadCancelled("User cancelled")
                self.log(f"\n▶ Nedlasting: {url}")
                self.prog(0.0, None, None, None)
                is_nrk_url = "nrk.no" in url.lower()
                if self.mode == "mp4":
                    merge_fmt, pp_key = ("mkv", "FFmpegVideoRemuxer") if is_nrk_url else ("mp4", "FFmpegVideoConvertor")
                    ydl_opts = {**base_opts, "format": fmt, "merge_output_format": merge_fmt, "postprocessors": [{"key": pp_key, "preferedformat": merge_fmt}]}
                elif self.mode == "mp3":
                    ydl_opts = {**base_opts, "format": fmt, "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": self.mp3_quality}, {"key": "EmbedThumbnail"}, {"key": "FFmpegMetadata"}], "writethumbnail": True}
                else:
                    ydl_opts = {**base_opts, "format": fmt}
                if self.browser and self.browser.lower() != "none":
                    ydl_opts["cookiesfrombrowser"] = (self.browser.lower(),)
                    self.log(f"Bruker cookies fra nettleser: {self.browser}")
                if self.playlist_items and self.playlist_items != "ASK":
                    ydl_opts["playlist_items"] = self.playlist_items
                with YoutubeDL(ydl_opts) as ydl:
                    self.log("Starter nedlasting…")
                    info = ydl.extract_info(url, download=False)
                    is_playlist = isinstance(info, dict) and info.get("entries") is not None
                    if is_playlist and self.playlist_items == "ASK":
                        approx_total = info.get("n_entries") or info.get("playlist_count") or "?"
                        self._request_playlist_decision(approx_total)
                        decision = self._pl_decision_q.get(timeout=3600)
                        if decision == "cancel": raise DownloadCancelled("User cancelled")
                        elif decision == "first": ydl.params["playlist_items"] = "1"
                        else: ydl.params.pop("playlist_items", None)
                    final_path = None
                    if not is_playlist and isinstance(info, dict):
                        prep_name = ydl.prepare_filename(info)
                        if self.mode == "mp3": final_path = Path(prep_name).with_suffix(".mp3")
                        elif self.mode == "mp4": final_path = Path(prep_name).with_suffix(".mkv" if is_nrk_url else ".mp4")
                        else: final_path = Path(prep_name)
                        if prep_name: self._last_filename = str(final_path)
                    elif is_playlist: self.log("📜 Playliste oppdaget – flere filer forventes.")
                    if not is_playlist and final_path and final_path.exists():
                        if not self.overwrites:
                            self.log(f"⚠ Fil finnes allerede – hopper over: {final_path.name}")
                            continue
                        else: self.log(f"↻ Overskriver eksisterende fil: {final_path.name}")
                    ydl.download([url])
                self.prog(100.0, None, None, self._last_filename)
                if self._last_filename: self.log(f"✅ Lagret: {Path(self._last_filename).name}")
                else: self.log("✅ Ferdig for denne URLen.")
                self._last_filename = None
            self.log(f"\n🎉 Alle nedlastinger fullført. Filer i: {self.out_dir}")
        except DownloadCancelled: self.log("⛔ Avbrutt.")
        except DownloadError as e: self.log(f"❌ Nedlastingsfeil: {e}")
        except FileNotFoundError: self.log("❌ FFmpeg ikke funnet. Legg ffmpeg.exe i samme mappe.")
        except Exception as e: self.log(f"❌ Uventet feil: {e}")


    def cancel(self):
        self._cancel = True


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        # Sett dark mode basert på konfigurasjon
        appearance_mode = "dark" if self.cfg.get("dark_mode", True) else "light"
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme("blue")
        self.title("Nedlastarn")
        self.geometry("980x720")
        self.minsize(820, 560)
       
        # Sentrer hovedvinduet på skjermen
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 980) // 2
        y = (screen_height - 720) // 2
        self.geometry(f"980x720+{x}+{y}")
       
        self.worker: Downloader | None = None
        self.msg_q: queue.Queue[str] = queue.Queue()
        self._build_ui()
        self._poll_messages()
        self._try_enable_dnd()
        self._update_nrk_hint()


    def _build_ui(self):
        pad = 10
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=pad, pady=pad)
        top_row = ctk.CTkFrame(container)
        top_row.pack(fill="x", padx=pad, pady=(pad, 5))
        ctk.CTkLabel(top_row, text="Nedlastarn", font=("Segoe UI", 16, "bold")).pack(side="left")
        ctk.CTkButton(top_row, text="Innstillinger", command=self._open_settings).pack(side="right", padx=(0,8))
        ctk.CTkButton(top_row, text="Om", width=70, command=self._show_about).pack(side="right")
        url_row = ctk.CTkFrame(container)
        url_row.pack(fill="both", expand=False, padx=pad, pady=5)
        ctk.CTkLabel(url_row, text="Video-URL(er) – én per linje").pack(anchor="w")
        self.url_box = ctk.CTkTextbox(url_row, height=160)
        self.url_box.pack(fill="x", expand=True)
        self.url_box.bind("<KeyRelease>", self._update_nrk_hint)
        btns = ctk.CTkFrame(url_row)
        btns.pack(fill="x", pady=(6, 0))
        ctk.CTkButton(btns, text="Lim inn", command=self._paste_clipboard).pack(side="left")
        ctk.CTkButton(btns, text="Tøm", command=lambda: (self.url_box.delete("1.0", tk.END), self._update_nrk_hint())).pack(side="left", padx=(8, 0))
        self.nrk_hint = ctk.CTkLabel(url_row, text="", wraplength=700)
        self.nrk_hint.pack(anchor="w", pady=(4, 0))
        dir_row = ctk.CTkFrame(container)
        dir_row.pack(fill="x", padx=pad, pady=5)
        ctk.CTkLabel(dir_row, text="Lagre til").pack(side="left", padx=(0, 8))
        self.dir_var = tk.StringVar(value=self.cfg.get("default_dir", DEFAULT_CONFIG["default_dir"]))
        self.dir_entry = ctk.CTkEntry(dir_row, textvariable=self.dir_var)
        self.dir_entry.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(dir_row, text="Bla gjennom…", command=self._choose_folder).pack(side="left", padx=(8, 0))
        row2 = ctk.CTkFrame(container)
        row2.pack(fill="x", padx=pad, pady=5)
        fmt_frame = ctk.CTkFrame(row2)
        fmt_frame.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(fmt_frame, text="Format").pack(anchor="w")
        self.format_var = tk.StringVar(value="mp4")
        for text, val in (("MP4 (video)", "mp4"), ("MP3 (kun lyd)", "mp3"), ("Behold original", "best")):
            ctk.CTkRadioButton(fmt_frame, text=text, value=val, variable=self.format_var, command=self._toggle_quality_state).pack(anchor="w")
        qual_frame = ctk.CTkFrame(row2)
        qual_frame.pack(side="left", padx=(8, 8))
        ctk.CTkLabel(qual_frame, text="Kvalitet").pack(anchor="w")
        self.quality_var = tk.StringVar(value="Beste")
        self.quality_box = ctk.CTkComboBox(qual_frame, variable=self.quality_var, state="readonly", values=["Beste", "1080p", "720p", "480p"])
        self.quality_box.pack()
        mp3_frame = ctk.CTkFrame(row2)
        mp3_frame.pack(side="left", padx=(8, 8))
        ctk.CTkLabel(mp3_frame, text="MP3-kvalitet (kbps)").pack(anchor="w")
        self.mp3_quality_var = tk.StringVar(value="192")
        self.mp3_quality_box = ctk.CTkComboBox(mp3_frame, variable=self.mp3_quality_var, state="disabled", values=["128", "192", "256", "320"])
        self.mp3_quality_box.pack()
        cookie_frame = ctk.CTkFrame(row2)
        cookie_frame.pack(side="left", padx=(8, 8))
        ctk.CTkLabel(cookie_frame, text="Cookies fra nettleser").pack(anchor="w")
        # Auto-detect browser hvis mulig
        detected_browser = autodetect_browser()
        browser_values = ["Ingen", "Chrome", "Edge", "Firefox"]
        default_browser = {"chrome": "Chrome", "edge": "Edge", "firefox": "Firefox"}.get(detected_browser, "Ingen")
        
        self.browser_var = tk.StringVar(value=default_browser)
        self.browser_box = ctk.CTkComboBox(cookie_frame, variable=self.browser_var, state="readonly", values=browser_values)
        self.browser_box.pack()
        pl_frame = ctk.CTkFrame(row2)
        pl_frame.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(pl_frame, text="Spillelistehåndtering").pack(anchor="w")
        self.pl_mode_var = tk.StringVar(value="Spør")
        self.pl_mode_box = ctk.CTkComboBox(pl_frame, variable=self.pl_mode_var, state="readonly", values=["Spør", "Alle", "Kun første"])
        self.pl_mode_box.pack()
        btn_row = ctk.CTkFrame(container)
        btn_row.pack(fill="x", padx=pad, pady=8)
        self.btn_start = ctk.CTkButton(btn_row, text="Last ned", command=self._start_download)
        self.btn_start.pack(side="left")
        self.btn_cancel = ctk.CTkButton(btn_row, text="Avbryt", command=self._cancel_download, state="disabled")
        self.btn_cancel.pack(side="left", padx=(8, 0))
        self.btn_open = ctk.CTkButton(btn_row, text="Åpne mappe", command=self._open_folder)
        self.btn_open.pack(side="left", padx=(8, 0))
        prog_frame = ctk.CTkFrame(container)
        prog_frame.pack(fill="x", padx=pad, pady=(5, 0))
        self.progbar = ctk.CTkProgressBar(prog_frame)
        self.progbar.set(0)
        self.progbar.pack(fill="x", expand=True, side="left", padx=(0, 10), pady=8)
        self.speed_label = ctk.CTkLabel(prog_frame, text="Hastighet: –   |   Gjenstår: –")
        self.speed_label.pack(side="left")
        self.current_item_label = ctk.CTkLabel(prog_frame, text="Element: –")
        self.current_item_label.pack(side="left", padx=(10, 0))
        log_frame = ctk.CTkFrame(container)
        log_frame.pack(fill="both", expand=True, padx=pad, pady=(5, pad))
        self.log = ctk.CTkTextbox(log_frame, state="disabled")
        self.log.pack(fill="both", expand=True)
        self._log("Klar. Lim inn én eller flere URLer og trykk 'Last ned'.")


    def _open_settings(self):
        win = ctk.CTkToplevel(self)
        win.title("Innstillinger")
        win.geometry("520x300")
        win.resizable(False, False)
        win.transient(self); win.grab_set()
        
        # Sentrer vinduet på hovedvinduet
        win.update_idletasks()  # Oppdater vinduet før vi beregner posisjon
        x = self.winfo_x() + (self.winfo_width() // 2) - (520 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (300 // 2)
        win.geometry(f"520x300+{x}+{y}")
        frm = ctk.CTkFrame(win); frm.pack(fill="both", expand=True, padx=14, pady=14)
        self.keep_norw_var = tk.BooleanVar(value=self.cfg.get("keep_norwegian_chars", False))
        ctk.CTkCheckBox(frm, text="Behold norske tegn i filnavn (æ/ø/å)", variable=self.keep_norw_var).pack(anchor="w", pady=(0,8))
        self.overwrite_var = tk.BooleanVar(value=self.cfg.get("overwrite_existing", False))
        ctk.CTkCheckBox(frm, text="Overskriv eksisterende filer", variable=self.overwrite_var).pack(anchor="w", pady=(0,8))
        self.dark_mode_var = tk.BooleanVar(value=self.cfg.get("dark_mode", True))
        ctk.CTkCheckBox(frm, text="Mørk modus", variable=self.dark_mode_var).pack(anchor="w", pady=(0,8))
        dir_row = ctk.CTkFrame(frm); dir_row.pack(fill="x", pady=(6,6))
        ctk.CTkLabel(dir_row, text="Standard lagringsmappe:").pack(anchor="w")
        self.cfg_dir_var = tk.StringVar(value=self.cfg.get("default_dir", DEFAULT_CONFIG["default_dir"]))
        ent = ctk.CTkEntry(dir_row, textvariable=self.cfg_dir_var); ent.pack(fill="x", expand=True, side="left")
        ctk.CTkButton(dir_row, text="Velg…", command=lambda: self._pick_cfg_dir(ent)).pack(side="left", padx=(8,0))
        btns = ctk.CTkFrame(frm); btns.pack(fill="x", pady=(10,0))
        ctk.CTkButton(btns, text="Lagre", command=lambda: self._save_settings(win)).pack(side="right")
        ctk.CTkButton(btns, text="Avbryt", command=win.destroy).pack(side="right", padx=(8,0))


    def _pick_cfg_dir(self, entry):
        path = filedialog.askdirectory(initialdir=self.cfg_dir_var.get() or str(Path.home()))
        if path: self.cfg_dir_var.set(path)


    def _save_settings(self, win):
        # Hent den nye verdien fra avkrysningsboksen
        new_dark_mode = bool(self.dark_mode_var.get())
        
        # Lagre alle innstillinger til fil
        self.cfg["keep_norwegian_chars"] = bool(self.keep_norw_var.get())
        self.cfg["overwrite_existing"] = bool(self.overwrite_var.get())
        self.cfg["dark_mode"] = new_dark_mode
        self.cfg["default_dir"] = self.cfg_dir_var.get() or DEFAULT_CONFIG["default_dir"]
        save_config(self.cfg)
        
        # Oppdater standardmappen i hovedvinduet
        self.dir_var.set(self.cfg["default_dir"])
        
        # --- HER ER ENDRINGEN ---
        # Bytt tema umiddelbart hvis det ble endret
        current_mode = ctk.get_appearance_mode().lower()
        new_mode_str = "dark" if new_dark_mode else "light"
        
        if current_mode != new_mode_str:
            ctk.set_appearance_mode(new_mode_str)
            self._log(f"Tema endret til {new_mode_str} modus.")
        else:
            self._log("Innstillinger lagret.")
        
        # Lukk innstillingsvinduet
        win.destroy()


    def _try_enable_dnd(self):
        try:
            self.url_box.drop_target_register("*")
            self.url_box.dnd_bind("<<Drop>>", self._on_drop)
            self._log("Drag & drop aktivert.")
        except Exception: pass


    def _on_drop(self, event):
        data = (getattr(event, "data", "") or "").strip().strip("{}")
        if data:
            self.url_box.insert(tk.END, data.replace("\r", "\n") + "\n")
        self._update_nrk_hint()


    def _update_nrk_hint(self, *_):
        content = self.url_box.get("1.0", tk.END).lower()
        if "nrk.no" in content: self.nrk_hint.configure(text="Tips: NRK-linker lagres som MKV for best kvalitet. Andre lagres som MP4.")
        else: self.nrk_hint.configure(text="")
           
    def _paste_clipboard(self):
        text = None
        
        # Prøv først pyperclip hvis tilgjengelig
        if HAS_PYPERCLIP:
            try:
                text = pyperclip.paste()
            except Exception:
                pass
        
        # Fallback til tkinter's clipboard_get
        if text is None:
            try:
                text = self.clipboard_get()
            except Exception:
                messagebox.showwarning("Lim inn", "Kunne ikke lese fra utklippstavlen.")
                return
        
        if text:
            self.url_box.insert(tk.END, text.strip() + "\n")
            self._update_nrk_hint()


    def _choose_folder(self):
        path = filedialog.askdirectory(initialdir=self.dir_var.get() or str(Path.home()))
        if path: self.dir_var.set(path)
           
    def _open_folder(self):
        try: os.startfile(self.dir_var.get())
        except Exception as e: messagebox.showerror("Åpne mappe", f"Kunne ikke åpne mappen.\n{e}")
           
    def _validate_urls(self, urls: list[str]):
        from urllib.parse import urlparse
        valid, invalid = [], []
        for u in urls:
            try:
                p = urlparse(u)
                if p.scheme in ("http", "https") and p.netloc: valid.append(u)
                else: invalid.append(u)
            except Exception: invalid.append(u)
        return valid, invalid
   
    def _set_ui_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for widget in [self.url_box, self.dir_entry, self.btn_start, self.btn_open]:
            widget.configure(state=state)
        self.browser_box.configure(state="readonly" if enabled else "disabled")
        self.quality_box.configure(state="readonly" if (enabled and self.format_var.get() != "mp3") else "disabled")
        self.mp3_quality_box.configure(state="readonly" if (enabled and self.format_var.get() == "mp3") else "disabled")
        for child in self.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                for grandchild in child.winfo_children():
                     if isinstance(grandchild, ctk.CTkRadioButton):
                         grandchild.configure(state=state)
        self.btn_cancel.configure(state="normal" if not enabled else "disabled")


    def _start_download(self):
        if self.worker and self.worker.is_alive():
            messagebox.showinfo("Opptatt", "En nedlasting kjører allerede.")
            return
        urls = [u.strip() for u in self.url_box.get("1.0", tk.END).splitlines() if u.strip()]
        if not urls:
            messagebox.showinfo("Mangler URL", "Lim inn minst én URL først.")
            return
        valid, invalid = self._validate_urls(urls)
        if invalid:
            messagebox.showerror("Ugyldige URLer", "Disse er ikke gyldige URLer:\n\n" + "\n".join(invalid))
            return
        
        # Sjekk FFmpeg før nedlasting starter
        if not _check_ffmpeg():
            messagebox.showerror("FFmpeg ikke funnet", 
                "FFmpeg er ikke tilgjengelig på systemet.\n\n"
                "Last ned ffmpeg.exe og legg den i samme mappe som programmet,\n"
                "eller installer FFmpeg systemvidt.")
            return
        out_dir = Path(self.dir_var.get())
        mode = self.format_var.get()
        quality = {"Beste": "best", "1080p": "1080p", "720p": "720p", "480p": "480p"}[self.quality_var.get()]
        browser = {"Ingen": "none", "Chrome": "chrome", "Edge": "edge", "Firefox": "firefox"}[self.browser_var.get()]
        pl_map = {"Alle": None, "Kun første": "1", "Spør": "ASK"}
        self._clear_log()
        self._set_progress(None)
        self.worker = Downloader(valid, out_dir, mode, quality, browser, self.cfg["keep_norwegian_chars"], self.cfg["overwrite_existing"], self.msg_q, mp3_quality=self.mp3_quality_var.get(), playlist_items=pl_map[self.pl_mode_var.get()])
        self.worker.start()
        self._set_ui_enabled(False)
        self._log("Starter…")


    def _cancel_download(self):
        if self.worker and self.worker.is_alive():
            self.worker.cancel()
            self.btn_cancel.configure(text="Avbryter...", state="disabled")
            self._log("Avbryter…")
           
    def _log(self, text: str):
        self.log.configure(state="normal")
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)
        self.log.configure(state="disabled")


    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.configure(state="disabled")


    def _poll_messages(self):
        try:
            while True:
                kind, *data = self.msg_q.get_nowait()
                if kind == "log": self._log(data[0])
                elif kind == "progress": self._set_progress(*data)
                elif kind == "ask_playlist":
                    ans = messagebox.askyesnocancel("Spilleliste funnet", f"Fant spilleliste (~{data[0]} videoer).\n\nLaste ned alle?\n\n(Ja=Alle, Nei=Kun første, Avbryt=Ingen)")
                    choice = "cancel" if ans is None else ("all" if ans else "first")
                    if self.worker: self.worker.set_playlist_decision(choice)
        except queue.Empty: pass
        if self.worker and not self.worker.is_alive():
            self._set_ui_enabled(True)
            self.btn_cancel.configure(text="Avbryt")  # Tilbakestill knapptekst
            self.worker = None
        self.after(100, self._poll_messages)


    def _fmt_eta(self, secs: int | None) -> str:
        if secs is None: return "–"
        secs = max(0, int(secs))
        h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
        return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"


    def _set_progress(self, pct: float | None, speed_bps: float = None, eta_s: int = None, filename: str = None, item_info: dict = None):
        if pct is None:
            self.progbar.set(0)
            self.speed_label.configure(text="Hastighet: –   |   Gjenstår: –")
            self.current_item_label.configure(text="Element: –")
            return
        self.progbar.set(max(0.0, min(100.0, pct)) / 100.0)
        spd_txt = f"{speed_bps/1024/1024:.2f} MB/s" if speed_bps else "–"
        self.speed_label.configure(text=f"Hastighet: {spd_txt}   |   Gjenstår: {self._fmt_eta(eta_s)}")
        if item_info and (item_info.get("title") or item_info.get("i") or item_info.get("n")):
            i, n, title = item_info.get("i"), item_info.get("n"), item_info.get("title")
            idx_txt = f"{i}/{n} – " if i and n else ""
            shown = title or (Path(filename).name if filename else "–")
            self.current_item_label.configure(text=f"Element: {idx_txt}{shown}")
        elif filename: 
            self.current_item_label.configure(text=f"Element: {Path(filename).name}")
        else: 
            self.current_item_label.configure(text="Element: –")


    def _toggle_quality_state(self):
        is_mp3 = self.format_var.get() == 'mp3'
        self.quality_box.configure(state='disabled' if is_mp3 else 'readonly')
        self.mp3_quality_box.configure(state='readonly' if is_mp3 else 'disabled')
        if self.worker and not self.worker.is_alive():
            self._set_ui_enabled(True)


    def _show_about(self):
        about = ctk.CTkToplevel(self)
        about.title("Om Nedlastarn")
        about.geometry("480x360")
        about.resizable(False, False)
        about.transient(self); about.grab_set(); about.lift(); about.focus_force()
       
        # Sentrer vinduet på hovedvinduet
        about.update_idletasks()  # Oppdater vinduet før vi beregner posisjon
        x = self.winfo_x() + (self.winfo_width() // 2) - (480 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (360 // 2)
        about.geometry(f"480x360+{x}+{y}")
       
        frame = ctk.CTkFrame(about)
        frame.pack(fill='both', expand=True, padx=16, pady=16)


        title_label = ctk.CTkLabel(frame, text="Nedlastarn", font=("Segoe UI", 16, "bold"))
        title_label.pack(anchor='w', pady=(0, 10))
       
        text_content = (
            "Dette programmet er et grafisk grensesnitt som bruker de\n"
            "kraftige kommandolinjeverktøyene yt-dlp og FFmpeg.\n\n"
            "All ære for selve nedlastingen og konverteringen går til\n"
            "utviklerne av disse fantastiske open source-prosjektene.\n\n"
            "Hovedfunksjoner:\n"
            "• Last ned fra tusenvis av nettsteder (YouTube, NRK etc.)\n"
            "• Lagre som MP4-video eller MP3-lyd\n"
            "• Bruk cookies fra nettleser for innloggede sider\n"
            "• Håndtering av spillelister"
        )
       
        info_label = ctk.CTkLabel(frame, text=text_content, justify='left')
        info_label.pack(anchor='w')
       
        ctk.CTkButton(frame, text='Lukk', command=about.destroy).pack(pady=(20,0))




if __name__ == "__main__":
    app = App()
    app.mainloop()

