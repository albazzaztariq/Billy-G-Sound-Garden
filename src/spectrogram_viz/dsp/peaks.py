import numpy as np


class PeakTracker:
    def __init__(self, decay: float = 0.85, top_n: int = 8) -> None:
        self._decay = float(decay)
        self._top_n = int(top_n)
        self._envelope: np.ndarray | None = None

    def update(self, spectrum_db: np.ndarray) -> np.ndarray:
        if self._envelope is None or self._envelope.shape != spectrum_db.shape:
            self._envelope = spectrum_db.copy()
        else:
            decayed = self._envelope * self._decay + (1 - self._decay) * spectrum_db.min()
            self._envelope = np.maximum(decayed, spectrum_db)
        return self._envelope

    def top_peaks(self, freqs: np.ndarray) -> list[tuple[float, float]]:
        if self._envelope is None:
            return []
        idx = np.argpartition(self._envelope, -self._top_n)[-self._top_n :]
        idx = idx[np.argsort(-self._envelope[idx])]
        return [(float(freqs[i]), float(self._envelope[i])) for i in idx]

    def reset(self) -> None:
        self._envelope = None
