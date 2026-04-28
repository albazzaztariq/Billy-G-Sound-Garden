import numpy as np
from scipy.signal import windows as _w

SUPPORTED_WINDOWS: tuple[str, ...] = ("hann", "hamming", "blackman", "rect")


def get_window(name: str, length: int) -> np.ndarray:
    name = name.lower()
    if name == "hann":
        return _w.hann(length, sym=False).astype(np.float32)
    if name == "hamming":
        return _w.hamming(length, sym=False).astype(np.float32)
    if name == "blackman":
        return _w.blackman(length, sym=False).astype(np.float32)
    if name == "rect":
        return np.ones(length, dtype=np.float32)
    raise ValueError(f"Unsupported window: {name}. Choose from {SUPPORTED_WINDOWS}")


def window_gain(window: np.ndarray) -> float:
    return float(np.sum(window) / window.size)


def apply_window(block: np.ndarray, window: np.ndarray) -> np.ndarray:
    return block * window
