import logging
import sys
from PyQt6 import QtCore, QtWidgets

from ..config import AudioConfig, SPLASH_IMAGE, SPLASH_DURATION_MS
from ..audio import AudioStream, RingBuffer, DeviceManager
from ..dsp import FFTAnalyzer, PeakTracker
from ..errors import DeviceNotFoundError, SampleRateMismatchError
from .spectrum_view import SpectrumView
from .splash import SplashScreen
from .icons import make_guitar_icon, set_windows_app_user_model_id

LOGGER = logging.getLogger(__name__)
TIMER_INTERVAL_MS = 16


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller: "AppController") -> None:
        super().__init__()
        self.setWindowTitle("Billy G Soundgarden — Spectrogram Viz")
        self.resize(1200, 700)
        self._controller = controller
        self.setCentralWidget(controller.spectrum_view)


class AppController:
    def __init__(self, config: AudioConfig) -> None:
        config.validate()
        self._config = config
        self._buffer = RingBuffer(capacity=max(config.sample_rate, config.fft_size * 4))
        self._stream = AudioStream(config, self._buffer)
        self._analyzer = FFTAnalyzer(config)
        self._peaks = PeakTracker()
        self._app: QtWidgets.QApplication | None = None
        self._window: MainWindow | None = None
        self._splash: SplashScreen | None = None
        self.spectrum_view: SpectrumView | None = None
        self._timer: QtCore.QTimer | None = None

    def run(self) -> int:
        print("[DEBUG] AppController.run: starting QApplication")
        set_windows_app_user_model_id()
        self._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        self._icon = make_guitar_icon()
        self._app.setWindowIcon(self._icon)

        self._splash = SplashScreen(SPLASH_IMAGE, duration_ms=SPLASH_DURATION_MS)
        self._splash.setWindowIcon(self._icon)
        self._splash.finished.connect(self._on_splash_done)
        self._splash.show()

        return self._app.exec()

    def _on_splash_done(self) -> None:
        print("[DEBUG] AppController._on_splash_done: building main window")
        self.spectrum_view = SpectrumView(self._analyzer.frequency_axis())
        self._window = MainWindow(self)
        self._window.setWindowIcon(self._icon)
        self._window.show()

        try:
            self._validate_device()
            self._stream.start()
        except (DeviceNotFoundError, SampleRateMismatchError) as e:
            QtWidgets.QMessageBox.critical(self._window, "Audio Device Error", str(e))
            self.shutdown()
            return

        self._timer = QtCore.QTimer(self._window)
        self._timer.setInterval(TIMER_INTERVAL_MS)
        self._timer.timeout.connect(self._on_timer_tick)
        self._timer.start()

    def _validate_device(self) -> None:
        dm = DeviceManager()
        if self._config.device_index is None:
            default = dm.get_default_input()
            print(f"[DEBUG] Using default input device: [{default.index}] {default.name}")
        else:
            dm.validate_device(self._config.device_index, self._config.sample_rate)

    def _on_timer_tick(self) -> None:
        block = self._buffer.latest(self._config.block_size)
        if block is None:
            return
        spectrum = self._analyzer.compute(block)
        envelope = self._peaks.update(spectrum)
        self.spectrum_view.update_spectrum(spectrum)
        self.spectrum_view.update_peaks(envelope)
        if self._stream.clip_detected():
            self.spectrum_view.set_clip(True)
            self._stream.reset_clip()
        else:
            self.spectrum_view.set_clip(False)

    def shutdown(self) -> None:
        print("[DEBUG] AppController.shutdown")
        if self._timer is not None:
            self._timer.stop()
        self._stream.stop()
        if self._app is not None:
            self._app.quit()
