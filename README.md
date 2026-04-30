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

## Roadmap / Ideas

- [x] **Real-time Spectrogram Visualization** — Use Python (with numpy and scipy) to analyze incoming audio from an interface and display a live FFT spectrum, useful for identifying resonant frequencies.
- [ ] **Sound Activated Recorder** — A Python-based project using PyAudio to create an automated recording script that starts recording only when audio surpasses a certain dB threshold, useful for live recordings.
- [ ] **Audio Source Separation Tool** — Use libraries like spleeter or nussl in Python to create a tool that separates a master recording into drums, bass, vocals, and other components for remixing.
- [ ] **Real-time Guitar Pedal** — Implement an equalizer or delay effect. Clip audio files.
- [ ] **Custom Waveshaper / Distortion Plugin** — An effect where the user can interactively draw or modify the wave-shaping curve to create unique saturation.
- [ ] **Polyphonic Synthesizer** — A synth with multiple oscillators (sine, square, saw, noise), filter, and ADSR envelope.
- [ ] **"Vintage" Processor** — A plugin that applies a vintage effect, simulating old radio or vinyl characteristics, using a combination of bandpass filtering and intentional noise/distortion.
- [ ] **MIDI Arpeggiator** — A program that takes MIDI input and outputs a customizable arpeggio pattern. Standalone application to feed into a DAW or as a plugin.
- [ ] **Intelligent Drum Humanizer** — A MIDI tool that takes rigid MIDI drum tracks and applies velocity/timing adjustments based on real drummer techniques (e.g., slightly ahead of the beat, harder velocity on stronger bars).
- [ ] **OSC Control Interface** — A GUI (using Python or JUCE) that sends Open Sound Control (OSC) messages to control hardware digital mixers or software like Ableton Live.

## License

MIT
