import threading
import numpy as np


class RingBuffer:
    """Thread-safe ring buffer of float32 samples; drops oldest on overrun."""

    def __init__(self, capacity: int, dtype=np.float32) -> None:
        self._capacity = int(capacity)
        self._data = np.zeros(self._capacity, dtype=dtype)
        self._write_idx = 0
        self._size = 0
        self._lock = threading.Lock()
        self._overruns = 0

    def write(self, block: np.ndarray) -> None:
        block = np.asarray(block).reshape(-1)
        n = block.size
        if n == 0:
            return
        with self._lock:
            if n >= self._capacity:
                self._data[:] = block[-self._capacity :]
                self._write_idx = 0
                self._size = self._capacity
                self._overruns += 1
                return
            end = self._write_idx + n
            if end <= self._capacity:
                self._data[self._write_idx : end] = block
            else:
                first = self._capacity - self._write_idx
                self._data[self._write_idx :] = block[:first]
                self._data[: n - first] = block[first:]
            self._write_idx = end % self._capacity
            new_size = self._size + n
            if new_size > self._capacity:
                self._overruns += 1
                self._size = self._capacity
            else:
                self._size = new_size

    def read(self, n: int) -> np.ndarray | None:
        with self._lock:
            if self._size < n:
                return None
            start = (self._write_idx - self._size) % self._capacity
            end = start + n
            if end <= self._capacity:
                out = self._data[start:end].copy()
            else:
                first = self._capacity - start
                out = np.concatenate((self._data[start:], self._data[: end - self._capacity]))
            self._size -= n
            return out

    def latest(self, n: int) -> np.ndarray | None:
        """Read the latest n samples without consuming."""
        with self._lock:
            if self._size < n:
                return None
            start = (self._write_idx - n) % self._capacity
            end = start + n
            if end <= self._capacity:
                return self._data[start:end].copy()
            first = self._capacity - start
            return np.concatenate((self._data[start:], self._data[: end - self._capacity]))

    def available(self) -> int:
        with self._lock:
            return self._size

    def overruns(self) -> int:
        with self._lock:
            return self._overruns

    def reset(self) -> None:
        with self._lock:
            self._write_idx = 0
            self._size = 0
            self._overruns = 0
            self._data[:] = 0
