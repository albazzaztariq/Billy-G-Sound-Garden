import numpy as np
import pyqtgraph as pg
from PyQt6 import QtCore, QtWidgets


class SpectrumView(QtWidgets.QWidget):
    def __init__(self, freqs: np.ndarray, parent=None) -> None:
        super().__init__(parent)
        self._freqs = freqs

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self._clip_indicator = QtWidgets.QLabel("CLIP", self)
        self._clip_indicator.setStyleSheet(
            "color: white; background-color: #333; padding: 2px 6px; border-radius: 3px;"
        )
        self._clip_indicator.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._clip_indicator.setFixedWidth(60)

        top = QtWidgets.QHBoxLayout()
        top.addStretch(1)
        top.addWidget(self._clip_indicator)
        layout.addLayout(top)

        self._plot = pg.PlotWidget()
        self._plot.setBackground("#0a0a0a")
        self._plot.setLabel("bottom", "Frequency", units="Hz")
        self._plot.setLabel("left", "Magnitude", units="dB")
        self._plot.setYRange(-100, 0)
        self._plot.setLogMode(x=True, y=False)
        self._plot.showGrid(x=True, y=True, alpha=0.3)
        self._curve = self._plot.plot(pen=pg.mkPen("#39ff14", width=1))
        self._peak_curve = self._plot.plot(pen=pg.mkPen("#ff8800", width=1, style=QtCore.Qt.PenStyle.DashLine))
        layout.addWidget(self._plot)

    def update_spectrum(self, spectrum_db: np.ndarray) -> None:
        f = self._freqs
        mask = f > 0
        self._curve.setData(f[mask], spectrum_db[mask])

    def update_peaks(self, envelope_db: np.ndarray) -> None:
        f = self._freqs
        mask = f > 0
        self._peak_curve.setData(f[mask], envelope_db[mask])

    def set_clip(self, clipping: bool) -> None:
        if clipping:
            self._clip_indicator.setStyleSheet(
                "color: white; background-color: #d40000; padding: 2px 6px; border-radius: 3px;"
            )
        else:
            self._clip_indicator.setStyleSheet(
                "color: white; background-color: #333; padding: 2px 6px; border-radius: 3px;"
            )
