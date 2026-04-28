import logging
import threading
import numpy as np
import sounddevice as sd
from ..config import AudioConfig
from .ring_buffer import RingBuffer

LOGGER = logging.getLogger(__name__)


class AudioStream:
    """Wraps sounddevice.InputStream and pushes blocks into a RingBuffer."""

    def __init__(self, config: AudioConfig, buffer: RingBuffer) -> None:
        self._config = config
        self._buffer = buffer
        self._stream: sd.InputStream | None = None
        self._clip_flag = threading.Event()
        self._running = threading.Event()

    def start(self) -> None:
        print("[DEBUG] AudioStream.start: opening InputStream")
        self._stream = sd.InputStream(
            samplerate=self._config.sample_rate,
            blocksize=self._config.block_size,
            channels=self._config.channels,
            device=self._config.device_index,
            dtype="float32",
            callback=self._callback,
        )
        self._stream.start()
        self._running.set()
        print(f"[DEBUG] AudioStream.start: running at {self._config.sample_rate} Hz")

    def stop(self) -> None:
        print("[DEBUG] AudioStream.stop")
        self._running.clear()
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception as e:
                LOGGER.warning("Error closing stream: %s", e)
            self._stream = None

    def is_running(self) -> bool:
        return self._running.is_set()

    def clip_detected(self) -> bool:
        return self._clip_flag.is_set()

    def reset_clip(self) -> None:
        self._clip_flag.clear()

    def _callback(self, indata: np.ndarray, frames: int, time_info, status) -> None:
        if status:
            LOGGER.debug("Audio status: %s", status)
        mono = indata[:, 0] if indata.ndim == 2 else indata
        if np.any(np.abs(mono) >= self._config.clip_threshold):
            self._clip_flag.set()
        self._buffer.write(mono)

    def __enter__(self) -> "AudioStream":
        self.start()
        return self

    def __exit__(self, *exc) -> None:
        self.stop()
