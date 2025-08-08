# ADB Music Controller

A simple Python Tkinter app to control Android music playback via ADB (Android Debug Bridge).  
Allows you to play/pause, skip tracks, adjust volume, and connect to your device over Wi-Fi.

---

## Features

- Play/Pause, Next, Previous, Fast Forward, Rewind controls  
- Volume Up and Down buttons  
- Display current playing song and artist info  
- Configure ADB over Wi-Fi by entering device IP  
- Show PC network IP configuration  
- Auto-refresh current track info every 5 seconds  
- Minimal and easy-to-use GUI
- EXE file for easy use

---

## Requirements

- Python 3.x (or Windows)  
- ADB installed and accessible in your system PATH  
- Android device with USB debugging enabled  
- For Wi-Fi control: device and PC on the same network
- For USB control: A high quality USB cable that supports data transfer

---

## Usage

1. Connect your Android device via USB and enable USB debugging.  
2. Run the script (or open the EXE):  
   ```bash
   python adb-music-controller.py
   ```
3. Use the buttons to control playback and volume.  
4. To connect via Wi-Fi:  
   - Click **Configure ADB IP**  
   - Enter your device’s IP address  
   - The app will attempt to connect over Wi-Fi on port 5555  

---

## Notes

- Make sure your device is authorized for ADB debugging.  
- The app reads playback info from Android's media session and updates every 5 seconds.
- The app does not include duration and current playback info (not widely supported)

---

## Troubleshooting

- If playback info does not update, ensure your device is connected and playing media.  
- For Wi-Fi connection issues, verify device IP and that the devices are on the same network.  
