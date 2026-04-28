from dataclasses import dataclass, field
from pathlib import Path
from .errors import InvalidFFTSizeError

DEFAULT_SAMPLE_RATE = 48000
DEFAULT_BLOCK_SIZE = 1024
DEFAULT_FFT_SIZE = 2048
DEFAULT_WINDOW = "hann"
DEFAULT_CHANNELS = 1
MAX_FFT_SIZE = 16384
DB_FLOOR = -120.0
CLIP_THRESHOLD = 0.99
SPLASH_DURATION_MS = 6000
ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"
SPLASH_IMAGE = ASSETS_DIR / "Billy G Startup.png"


@dataclass(frozen=True)
class AudioConfig:
    sample_rate: int = DEFAULT_SAMPLE_RATE
    block_size: int = DEFAULT_BLOCK_SIZE
    fft_size: int = DEFAULT_FFT_SIZE
    window: str = DEFAULT_WINDOW
    device_index: int | None = None
    channels: int = DEFAULT_CHANNELS
    db_floor: float = DB_FLOOR
    clip_threshold: float = CLIP_THRESHOLD

    def validate(self) -> None:
        if self.fft_size < self.block_size:
            raise InvalidFFTSizeError(
                f"fft_size ({self.fft_size}) must be >= block_size ({self.block_size})"
            )
        if self.fft_size > MAX_FFT_SIZE:
            raise InvalidFFTSizeError(f"fft_size ({self.fft_size}) > MAX_FFT_SIZE ({MAX_FFT_SIZE})")

    @classmethod
    def default(cls) -> "AudioConfig":
        return cls()
