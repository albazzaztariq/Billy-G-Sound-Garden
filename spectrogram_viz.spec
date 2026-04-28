# PyInstaller spec — works on Windows and macOS.
# Build:
#   Windows: pyinstaller spectrogram_viz.spec
#   macOS:   pyinstaller spectrogram_viz.spec
import sys
from pathlib import Path
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None
PROJECT = Path(SPECPATH)
ASSETS = PROJECT / "assets"

is_mac = sys.platform == "darwin"
is_win = sys.platform == "win32"

icon_path = None
if is_win and (ASSETS / "guitar.ico").exists():
    icon_path = str(ASSETS / "guitar.ico")
elif is_mac and (ASSETS / "guitar.icns").exists():
    icon_path = str(ASSETS / "guitar.icns")

binaries = collect_dynamic_libs("sounddevice")

datas = [
    (str(ASSETS / "Billy G Startup.png"), "assets"),
    (str(ASSETS / "guitar.png"), "assets"),
]
if (ASSETS / "guitar.ico").exists():
    datas.append((str(ASSETS / "guitar.ico"), "assets"))
if (ASSETS / "guitar.icns").exists():
    datas.append((str(ASSETS / "guitar.icns"), "assets"))

a = Analysis(
    ["src/spectrogram_viz/__main__.py"],
    pathex=["src"],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        "spectrogram_viz",
        "spectrogram_viz.audio",
        "spectrogram_viz.dsp",
        "spectrogram_viz.ui",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "PIL"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SpectrogramViz",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="SpectrogramViz",
)

if is_mac:
    app = BUNDLE(
        coll,
        name="SpectrogramViz.app",
        icon=icon_path,
        bundle_identifier="com.billygsoundgarden.spectrogramviz",
        info_plist={
            "CFBundleName": "Spectrogram Viz",
            "CFBundleDisplayName": "Billy G Soundgarden — Spectrogram Viz",
            "CFBundleShortVersionString": "0.1.0",
            "CFBundleVersion": "0.1.0",
            "NSHighResolutionCapable": "True",
            "NSMicrophoneUsageDescription": "Spectrogram Viz needs microphone access to display the live audio spectrum.",
            "LSMinimumSystemVersion": "11.0",
        },
    )
