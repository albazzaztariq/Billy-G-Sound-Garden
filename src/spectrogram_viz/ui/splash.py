from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets


class SplashScreen(QtWidgets.QWidget):
    """Frameless centered splash window. Shows an image full-window for `duration_ms`,
    then emits `finished` and closes."""

    finished = QtCore.pyqtSignal()

    def __init__(self, image_path: Path, duration_ms: int = 6000, target_size=(900, 600)) -> None:
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.SplashScreen
            | QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)

        pix = QtGui.QPixmap(str(image_path))
        if pix.isNull():
            print(f"[DEBUG] SplashScreen: failed to load {image_path}")
            self._pixmap = QtGui.QPixmap(*target_size)
            self._pixmap.fill(QtGui.QColor("#111"))
        else:
            self._pixmap = pix.scaled(
                target_size[0],
                target_size[1],
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

        self.resize(self._pixmap.size())
        self._center_on_screen()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        label = QtWidgets.QLabel(self)
        label.setPixmap(self._pixmap)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._on_done)
        self._timer.start(duration_ms)

    def _center_on_screen(self) -> None:
        screen = QtGui.QGuiApplication.primaryScreen()
        if screen is None:
            return
        geo = screen.availableGeometry()
        fr = self.frameGeometry()
        fr.moveCenter(geo.center())
        self.move(fr.topLeft())

    def _on_done(self) -> None:
        print("[DEBUG] SplashScreen: timeout fired")
        self.finished.emit()
        self.close()
