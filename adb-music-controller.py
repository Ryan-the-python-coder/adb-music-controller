import subprocess
import shutil
import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
import re

# Hide command window (on Windows)
STARTUPINFO = None
if sys.platform == "win32":
    STARTUPINFO = subprocess.STARTUPINFO()
    STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Locate adb
ADB_EXECUTABLE = shutil.which("adb")
if not ADB_EXECUTABLE:
    local_adb = os.path.join(os.getcwd(), "platform-tools", "adb.exe")
    if os.path.exists(local_adb):
        ADB_EXECUTABLE = local_adb

if not ADB_EXECUTABLE:
    messagebox.showerror(
        "ADB Not Found",
        "ADB is not installed and could not be found in the app folder.\n\n"
        "Please install ADB or include it in a 'platform-tools' folder next to this app."
    )
    sys.exit(1)

# Key events
KEY_EVENTS = {
    "Play/Pause": "KEYCODE_MEDIA_PLAY_PAUSE",
    "Next Track": "KEYCODE_MEDIA_NEXT",
    "Previous Track": "KEYCODE_MEDIA_PREVIOUS",
    "Volume Up": "KEYCODE_VOLUME_UP",
    "Volume Down": "KEYCODE_VOLUME_DOWN",
    "Fast Forward": "KEYCODE_MEDIA_FAST_FORWARD",
    "Rewind": "KEYCODE_MEDIA_REWIND",
}

class ADBMusicControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Music Controller")
        self.root.geometry("300x700")
        self.root.resizable(False, True)

        title = tk.Label(root, text="ADB Music Controller", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(15, 5))

        warning = tk.Label(
            root,
            text=(
                "⚠️ Make sure your Android device is connected\n"
                "and ADB debugging is enabled."
            ),
            font=("Segoe UI", 10),
            fg="red",
            justify="center"
        )
        warning.pack(pady=(0, 10))

        self.status_label = tk.Label(root, text="Loading...", font=("Segoe UI", 10), justify="center")
        self.status_label.pack(pady=(0, 20))

        for label, keycode in KEY_EVENTS.items():
            btn = tk.Button(root, text=label, width=22, height=2,
                            command=lambda k=keycode: self.send_keyevent(k))
            btn.pack(pady=6)

        self.ipconfig_btn = tk.Button(root, text="Show IP Config", width=22, height=2, command=self.show_ip_config)
        self.ipconfig_btn.pack(pady=10)

        self.wifi_connect_btn = tk.Button(root, text="Configure ADB IP", width=22, height=2, command=self.configure_adb_ip)
        self.wifi_connect_btn.pack(pady=10)

        self.update_playback_info()

    def send_keyevent(self, keycode):
        try:
            subprocess.run(
                [ADB_EXECUTABLE, "shell", "input", "keyevent", keycode],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
                startupinfo=STARTUPINFO
            )
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", f"Failed to send key event: {keycode}")
        self.update_playback_info()

    def update_playback_info(self):
        output = self.get_media_session_output()
        desc, _, _ = self.parse_media_session(output)
        wrapped_desc = self.wrap_text(self.sanitize_text(desc), 30)
        self.status_label.config(text=f"Playing:\n{wrapped_desc}")
        self.root.after(5000, self.update_playback_info)

    def sanitize_text(self, text):
        # Replace curly apostrophes with straight ones
        return text.replace("’", "'")

    def get_media_session_output(self):
        try:
            result = subprocess.run(
                [ADB_EXECUTABLE, "shell", "dumpsys", "media_session"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                startupinfo=STARTUPINFO
            )
            # Decode bytes explicitly as UTF-8, replace errors
            return result.stdout.decode('utf-8', errors='replace')
        except subprocess.SubprocessError:
            return ""

    def parse_media_session(self, output):
        desc_match = re.search(r'description=([^",\n]+(?:, [^",\n]+)*)', output)
        description = desc_match.group(1).strip() if desc_match else "Unknown Title/Artist"

        pos_match = re.search(r"PlaybackState.*position=(\d+)", output)
        pos_ms = int(pos_match.group(1)) if pos_match else 0

        dur_match = re.search(r"duration=(\d+)", output)
        dur_ms = int(dur_match.group(1)) if dur_match else 0

        return description, pos_ms, dur_ms

    def wrap_text(self, text, width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return "\n".join(lines)

    def show_ip_config(self):
        try:
            result = subprocess.run(
                ["ipconfig"] if sys.platform == "win32" else ["ifconfig"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                startupinfo=STARTUPINFO
            )
            ip_output = result.stdout.strip()
            messagebox.showinfo("IP Configuration", ip_output[:2000])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get IP config: {e}")

    def configure_adb_ip(self):
        ip = simpledialog.askstring("Configure ADB over IP", "Enter device IP address:")
        if ip:
            try:
                subprocess.run(
                    [ADB_EXECUTABLE, "tcpip", "5555"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                    startupinfo=STARTUPINFO
                )
                subprocess.run(
                    [ADB_EXECUTABLE, "connect", ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                    startupinfo=STARTUPINFO
                )
                messagebox.showinfo("Success", f"Connected to {ip} over Wi-Fi!")
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Failed to connect to device over Wi-Fi.")

def main():
    root = tk.Tk()
    app = ADBMusicControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()
