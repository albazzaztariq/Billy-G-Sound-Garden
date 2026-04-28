import numpy as np
from ..config import AudioConfig
from .windows import get_window, window_gain
from .scaling import db


class FFTAnalyzer:
    def __init__(self, config: AudioConfig) -> None:
        config.validate()
        self._config = config
        self._fft_size = config.fft_size
        self._window = get_window(config.window, config.block_size)
        self._window_gain = window_gain(self._window)
        self._freqs = np.fft.rfftfreq(self._fft_size, d=1.0 / config.sample_rate).astype(np.float32)

    @property
    def fft_size(self) -> int:
        return self._fft_size

    def bin_count(self) -> int:
        return self._freqs.size

    def frequency_axis(self) -> np.ndarray:
        return self._freqs

    def magnitude(self, block: np.ndarray) -> np.ndarray:
        n = block.size
        windowed = block[: self._config.block_size] * self._window[:n]
        if self._fft_size > windowed.size:
            padded = np.zeros(self._fft_size, dtype=np.float32)
            padded[: windowed.size] = windowed
            windowed = padded
        spec = np.fft.rfft(windowed, n=self._fft_size)
        mag = np.abs(spec) / (self._fft_size * self._window_gain + 1e-12)
        return mag.astype(np.float32)

    def compute(self, block: np.ndarray) -> np.ndarray:
        return db(self.magnitude(block), floor_db=self._config.db_floor)
