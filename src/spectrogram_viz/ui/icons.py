import sys
from pathlib import Path
from PyQt6 import QtCore, QtGui

from ..config import ASSETS_DIR

APP_USER_MODEL_ID = "BillyG.Soundgarden.SpectrogramViz.1"
GUITAR_PNG = ASSETS_DIR / "guitar.png"
GUITAR_ICO = ASSETS_DIR / "guitar.ico"
GUITAR_ICNS = ASSETS_DIR / "guitar.icns"


def set_windows_app_user_model_id(app_id: str = APP_USER_MODEL_ID) -> None:
    """Set the Windows AppUserModelID so the taskbar uses our icon, not python.exe.
    No-op on non-Windows platforms."""
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        print(f"[DEBUG] AppUserModelID set: {app_id}")
    except Exception as e:
        print(f"[DEBUG] Failed to set AppUserModelID: {e}")


def _load_first_existing(paths: list[Path]) -> QtGui.QIcon | None:
    for p in paths:
        if p.exists():
            print(f"[DEBUG] icons: loading {p}")
            ic = QtGui.QIcon(str(p))
            if not ic.isNull():
                return ic
    return None


def make_guitar_icon() -> QtGui.QIcon:
    """Load the guitar icon. Prefers platform-native format (.ico on Windows,
    .icns on macOS, .png everywhere as fallback). Falls back to a runtime
    emoji-painted pixmap if no asset is found."""
    if sys.platform == "win32":
        order = [GUITAR_ICO, GUITAR_PNG]
    elif sys.platform == "darwin":
        order = [GUITAR_ICNS, GUITAR_PNG]
    else:
        order = [GUITAR_PNG, GUITAR_ICO]

    icon = _load_first_existing(order)
    if icon is not None:
        return icon

    print("[DEBUG] icons: no asset found, painting fallback")
    pix = QtGui.QPixmap(256, 256)
    pix.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(pix)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)
    font = QtGui.QFont("Segoe UI Emoji" if sys.platform == "win32" else "Apple Color Emoji")
    font.setPixelSize(200)
    painter.setFont(font)
    painter.drawText(
        QtCore.QRectF(0, 0, 256, 256),
        int(QtCore.Qt.AlignmentFlag.AlignCenter),
        "\U0001F3B8",
    )
    painter.end()
    return QtGui.QIcon(pix)
