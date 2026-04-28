# Billy G Sound Garden — Spectrogram Viz

Real-time FFT spectrum visualizer for guitarists and audio engineers. Live-monitor your input device, identify resonant frequencies, and watch peaks decay in real time.

![Splash](assets/Billy%20G%20Startup.png)

## Download & Install

Grab the installer for your OS from the [latest Release](https://github.com/albazzaztariq/Billy-G-Sound-Garden/releases/latest):

- **Windows:** `SpectrogramViz-Setup-<version>.exe` — double-click and follow the wizard.
- **macOS:** `SpectrogramViz-macOS.dmg` — open, drag the app to Applications.

Everything (Python, PyQt6, sounddevice, etc.) is bundled inside the installer. No separate downloads needed.

## Features

- 6-second branded splash on launch
- Live FFT spectrum, log-frequency axis, dB magnitude
- Peak-hold envelope with configurable decay
- Clip indicator
- Configurable sample rate, block size, FFT size, window function (Hann / Hamming / Blackman / Rect)
- Cross-platform: Windows 10+, macOS 11+

## Run from source

```bash
git clone https://github.com/albazzaztariq/Billy-G-Sound-Garden.git
cd Billy-G-Sound-Garden
python -m pip install -r requirements.txt
PYTHONPATH=src python -m spectrogram_viz -v
```

## Build installers locally

```bash
python tools/make_icon.py            # generate guitar.ico / .icns / .png
pyinstaller --noconfirm spectrogram_viz.spec

# Windows: also run Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\installer.iss

# macOS: package as .dmg
create-dmg --volname "Spectrogram Viz" --app-drop-link 380 180 \
           "installer/Output/SpectrogramViz-macOS.dmg" "dist/SpectrogramViz.app"
```

## CI

Pushes to `main` build artifacts via GitHub Actions for both Windows and macOS. Tagging `v*` cuts a Release with the installers attached.

## License

MIT
