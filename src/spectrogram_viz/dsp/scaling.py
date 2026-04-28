import numpy as np


def db(magnitude: np.ndarray, ref: float = 1.0, floor_db: float = -120.0) -> np.ndarray:
    floor_lin = 10 ** (floor_db / 20.0) * ref
    safe = np.maximum(magnitude, floor_lin)
    return 20.0 * np.log10(safe / ref)


def amplitude_to_db(amp: np.ndarray, floor_db: float = -120.0) -> np.ndarray:
    return db(np.abs(amp), ref=1.0, floor_db=floor_db)


def detect_clipping(block: np.ndarray, threshold: float) -> bool:
    return bool(np.any(np.abs(block) >= threshold))


def normalize(values: np.ndarray, lo: float, hi: float) -> np.ndarray:
    if hi <= lo:
        return np.zeros_like(values)
    return np.clip((values - lo) / (hi - lo), 0.0, 1.0)
