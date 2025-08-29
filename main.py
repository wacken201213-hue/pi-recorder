import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import threading
import time
import re
import math
import struct

# Einstellungen
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
BUTTON_FONT = ("Arial", 18, "bold")
SMALL_FONT = ("Arial", 14, "bold")
TIME_FONT = ("Arial", 16, "bold")


# ffmpeg Audio-Aufnahme
import datetime

audio_proc = None
audio_start_time = None
audio_level_proc = None
current_audio_level = 0

def get_audio_level():
    """Überwacht kontinuierlich den Audio-Pegel mit arecord"""
    global audio_level_proc, current_audio_level
    
    try:
        # Einfacher Audio-Level-Monitor mit arecord
        cmd = ['arecord', '-D', 'plughw:1,0', '-f', 'S16_LE', '-r', '44100', '-t', 'raw']
        
        audio_level_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Einfache Level-Simulation basierend auf Audio-Input
        buffer_size = 4096
        while audio_level_proc and audio_level_proc.poll() is None:
            try:
                data = audio_level_proc.stdout.read(buffer_size)
                if data:
                    # Simple RMS-Berechnung für Audio-Level
                    import struct
                    samples = struct.unpack(f'<{len(data)//2}h', data)
                    rms = math.sqrt(sum(x*x for x in samples) / len(samples))
                    # Normalisierung auf 0-100%
                    current_audio_level = min(100, (rms / 32767) * 100 * 5)  # Verstärkung x5
                else:
                    current_audio_level = 0
                time.sleep(0.1)  # 10Hz Update-Rate
            except:
                current_audio_level = 0
                break
                
    except Exception as e:
        print(f"Audio-Level Monitoring Fehler: {e}")
        current_audio_level = 0

def start_audio_level_monitoring():
    """Startet das Audio-Level-Monitoring in einem Thread"""
    global audio_level_proc
    if audio_level_proc is None or audio_level_proc.poll() is not None:
        threading.Thread(target=get_audio_level, daemon=True).start()

def stop_audio_level_monitoring():
    """Stoppt das Audio-Level-Monitoring"""
    global audio_level_proc, current_audio_level
    if audio_level_proc:
        try:
            audio_level_proc.terminate()
            audio_level_proc.wait(timeout=2)
        except:
            pass
        audio_level_proc = None
    current_audio_level = 0

def start_audio_recording():
    global audio_proc, audio_start_time
    if audio_proc is not None and audio_proc.poll() is None:
        return
    # Dateinamen abfragen
    root = tk._default_root
    filename = simpledialog.askstring("Dateiname", "Dateiname für die Audioaufnahme (z.B. audio1.wav):", parent=root)
    if not filename:
        return
    if not filename.lower().endswith(".wav"):
        filename += ".wav"
    audio_cmd = [
        "ffmpeg", "-y", "-f", "alsa", "-i", "plughw:1,0", 
        "-c:a", "pcm_s32le", 
        "-ar", "44100", 
        "-ac", "2",
        filename
    ]
    def run_audio_ffmpeg():
        global audio_proc, audio_start_time
        try:
            audio_proc = subprocess.Popen(audio_cmd)
            audio_start_time = time.time()
        except Exception as e:
            messagebox.showerror("Fehler", f"ffmpeg Audio konnte nicht gestartet werden:\n{e}")
    threading.Thread(target=run_audio_ffmpeg, daemon=True).start()

def stop_audio_recording():
    global audio_proc, audio_start_time
    if audio_proc is not None and audio_proc.poll() is None:
        audio_proc.terminate()
        audio_proc = None
        audio_start_time = None

# ffmpeg Videoaufnahme

ffmpeg_proc = None

def start_video_recording():
    global ffmpeg_proc
    if ffmpeg_proc is not None and ffmpeg_proc.poll() is None:
        return
    # Dateinamen abfragen
    root = tk._default_root
    filename = simpledialog.askstring("Dateiname", "Dateiname für die Aufnahme (z.B. video1.mp4):", parent=root)
    if not filename:
        return
    if not filename.lower().endswith(".mp4"):
        filename += ".mp4"
    ffmpeg_cmd = [
        "ffmpeg", "-y", "-f", "v4l2", "-framerate", "25", "-video_size", "720x576", "-i", "/dev/video0",
        "-f", "alsa", "-i", "hw:2,0", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", filename
    ]
    def run_ffmpeg():
        global ffmpeg_proc
        try:
            ffmpeg_proc = subprocess.Popen(ffmpeg_cmd)
        except Exception as e:
            messagebox.showerror("Fehler", f"ffmpeg konnte nicht gestartet werden:\n{e}")
    threading.Thread(target=run_ffmpeg, daemon=True).start()

def stop_video_recording():
    global ffmpeg_proc
    if ffmpeg_proc is not None and ffmpeg_proc.poll() is None:
        ffmpeg_proc.terminate()
        ffmpeg_proc = None

# --- Menü-Logik ---
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pi Recorder")
        self.root.geometry("800x480")
        self.root.configure(bg="#222222")
        self.root.attributes('-fullscreen', True)
        
        # ESC-Taste zum Beenden
        self.root.bind('<Escape>', self.quit_app)
        # F11 zum Vollbild umschalten
        self.root.bind('<F11>', self.toggle_fullscreen)
        
        # Aufnahme-Prozesse
        self.video_process = None
        self.audio_process = None
        
        # Zeit-Tracking
        self.video_start_time = None
        self.audio_start_time = None
        
        self.show_main_menu()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def quit_app(self, event=None):
        """Beendet die Anwendung (ESC-Taste)"""
        # Alle laufenden Aufnahmen stoppen
        global audio_proc, ffmpeg_proc
        if audio_proc is not None:
            audio_proc.terminate()
        if ffmpeg_proc is not None:
            ffmpeg_proc.terminate()
        
        # Audio-Level-Monitoring stoppen
        stop_audio_level_monitoring()
        
        self.root.quit()
        self.root.destroy()

    def toggle_fullscreen(self, event=None):
        """Vollbild umschalten (F11-Taste)"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)

    def minimize_app(self):
        """Minimiert die Anwendung"""
        self.root.attributes('-fullscreen', False)
        self.root.iconify()

    def show_main_menu(self):
        # Audio-Level-Monitoring stoppen wenn wir das Audio-Menü verlassen
        stop_audio_level_monitoring()
        
        self.clear()
        frame = tk.Frame(self.root, bg="#222222")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        frame.grid_rowconfigure(0, weight=3)  # Hauptbuttons
        frame.grid_rowconfigure(1, weight=1)  # Control-buttons
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Hauptbuttons (Audio/Video)
        btn_audio = tk.Button(frame, text="Audio", font=BUTTON_FONT, bg="#4CAF50", fg="white", command=self.show_audio_menu)
        btn_audio.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        btn_video = tk.Button(frame, text="Video", font=BUTTON_FONT, bg="#2196F3", fg="white", command=self.show_video_menu)
        btn_video.grid(row=0, column=1, sticky="nsew", padx=10, pady=(10, 5))

        # Control-Buttons (kleiner, unterhalb)
        btn_minimize = tk.Button(frame, text="− Minimieren", font=SMALL_FONT, bg="#FF9800", fg="white", command=self.minimize_app)
        btn_minimize.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

        btn_exit = tk.Button(frame, text="× Beenden", font=SMALL_FONT, bg="#F44336", fg="white", command=self.quit_app)
        btn_exit.grid(row=1, column=1, sticky="ew", padx=10, pady=(5, 10))

    def show_audio_menu(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#222222")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        frame.grid_rowconfigure(0, weight=3)  # Aufnahme-Buttons
        frame.grid_rowconfigure(1, weight=1)  # Laufzeit-Anzeige
        frame.grid_rowconfigure(2, weight=1)  # Audio-Level
        frame.grid_rowconfigure(3, weight=1)  # Control-Buttons
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Aufnahme-Buttons
        btn_record = tk.Button(frame, text="Aufnahme starten", font=BUTTON_FONT, bg="#4CAF50", fg="white", command=start_audio_recording)
        btn_record.grid(row=0, column=0, sticky="nsew", padx=8, pady=(10, 5))

        btn_stop = tk.Button(frame, text="Aufnahme stoppen", font=BUTTON_FONT, bg="#F44336", fg="white", command=stop_audio_recording)
        btn_stop.grid(row=0, column=1, sticky="nsew", padx=8, pady=(10, 5))

        # Laufzeit-Anzeige
        self.audio_time_label = tk.Label(frame, text="Laufzeit: 00:00", font=TIME_FONT, bg="#222222", fg="white")
        self.audio_time_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=5)
        
        # Audio-Level Anzeige
        level_frame = tk.Frame(frame, bg="#222222")
        level_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=8, pady=5)
        
        tk.Label(level_frame, text="Audio Level:", font=("Arial", 12), 
                bg="#222222", fg="white").pack()
        
        self.audio_level_canvas = tk.Canvas(
            level_frame, 
            width=400, 
            height=25, 
            bg="#1a1a1a",
            highlightthickness=1,
            highlightbackground="#666666"
        )
        self.audio_level_canvas.pack(pady=5)
        
        # Startet das Audio-Level-Monitoring
        start_audio_level_monitoring()
        
        self.update_audio_time()

        # Control-Buttons
        btn_back = tk.Button(frame, text="← Zurück", font=SMALL_FONT, bg="#888888", fg="white", command=self.show_main_menu)
        btn_back.grid(row=3, column=0, sticky="ew", padx=8, pady=(5, 10))

        btn_exit = tk.Button(frame, text="× Beenden", font=SMALL_FONT, bg="#F44336", fg="white", command=self.quit_app)
        btn_exit.grid(row=3, column=1, sticky="ew", padx=8, pady=(5, 10))

    def show_video_menu(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#222222")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        frame.grid_rowconfigure(0, weight=3)  # Aufnahme-Buttons
        frame.grid_rowconfigure(1, weight=1)  # Laufzeit-Anzeige
        frame.grid_rowconfigure(2, weight=1)  # Control-Buttons
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Aufnahme-Buttons
        btn_start = tk.Button(frame, text="Video Start", font=BUTTON_FONT, bg="#4CAF50", fg="white", command=start_video_recording)
        btn_start.grid(row=0, column=0, sticky="nsew", padx=8, pady=(10, 5))

        btn_stop = tk.Button(frame, text="Video Stop", font=BUTTON_FONT, bg="#F44336", fg="white", command=stop_video_recording)
        btn_stop.grid(row=0, column=1, sticky="nsew", padx=8, pady=(10, 5))

        # Laufzeit-Anzeige
        self.video_time_label = tk.Label(frame, text="Laufzeit: 00:00", font=TIME_FONT, bg="#222222", fg="white")
        self.video_time_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=5)
        
        self.update_video_time()

        # Control-Buttons
        btn_back = tk.Button(frame, text="← Zurück", font=SMALL_FONT, bg="#888888", fg="white", command=self.show_main_menu)
        btn_back.grid(row=2, column=0, sticky="ew", padx=8, pady=(5, 10))

        btn_exit = tk.Button(frame, text="× Beenden", font=SMALL_FONT, bg="#F44336", fg="white", command=self.quit_app)
        btn_exit.grid(row=2, column=1, sticky="ew", padx=8, pady=(5, 10))

    def update_audio_time(self):
        """Aktualisiert die Laufzeit-Anzeige für Audio"""
        if hasattr(self, 'audio_time_label') and self.audio_time_label.winfo_exists():
            global audio_start_time
            if audio_start_time is not None:
                elapsed = int(time.time() - audio_start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                time_text = f"Laufzeit: {minutes:02d}:{seconds:02d}"
            else:
                time_text = "Laufzeit: 00:00"
            
            self.audio_time_label.config(text=time_text)
            
            # Audio-Level-Anzeige aktualisieren
            self.update_audio_level_display()
            
            self.root.after(1000, self.update_audio_time)
    
    def update_audio_level_display(self):
        """Aktualisiert das Audio-Level-Display"""
        if hasattr(self, 'audio_level_canvas') and self.audio_level_canvas.winfo_exists():
            try:
                self.audio_level_canvas.delete("all")
                
                # Canvas-Dimensionen
                canvas_width = 400
                canvas_height = 25
                
                # Hintergrund
                self.audio_level_canvas.create_rectangle(
                    0, 0, canvas_width, canvas_height, 
                    fill="#1a1a1a", outline="#666666"
                )
                
                # Level-Balken
                if current_audio_level > 0:
                    level_width = int((current_audio_level / 100) * (canvas_width - 4))
                    
                    # Farbe basierend auf Pegel
                    if current_audio_level < 50:
                        color = "#4CAF50"  # Grün
                    elif current_audio_level < 80:
                        color = "#FFC107"  # Gelb
                    else:
                        color = "#F44336"  # Rot
                    
                    self.audio_level_canvas.create_rectangle(
                        2, 2, 2 + level_width, canvas_height - 2,
                        fill=color, outline=""
                    )
                
                # Skalierung (25%, 50%, 75%, 100%)
                for i in [25, 50, 75, 100]:
                    x = int((i / 100) * (canvas_width - 4)) + 2
                    self.audio_level_canvas.create_line(
                        x, 0, x, canvas_height,
                        fill="#666666", width=1
                    )
                
                # Level-Text
                level_text = f"{current_audio_level:.0f}%"
                self.audio_level_canvas.create_text(
                    canvas_width // 2, canvas_height // 2,
                    text=level_text, fill="white", font=("Arial", 10, "bold")
                )
                
            except Exception as e:
                print(f"Level-Display Update Fehler: {e}")

    def update_video_time(self):
        """Aktualisiert die Laufzeit-Anzeige für Video"""
        if hasattr(self, 'video_time_label') and self.video_time_label.winfo_exists():
            if self.video_start_time is not None:
                elapsed = int(time.time() - self.video_start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                time_text = f"Laufzeit: {minutes:02d}:{seconds:02d}"
            else:
                time_text = "Laufzeit: 00:00"
            
            self.video_time_label.config(text=time_text)
            self.root.after(1000, self.update_video_time)

# --- Main ---
if __name__ == "__main__":
    app = App()
    app.root.mainloop()