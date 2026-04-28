import argparse
import logging
import sys
from .config import AudioConfig, DEFAULT_SAMPLE_RATE, DEFAULT_BLOCK_SIZE, DEFAULT_FFT_SIZE, DEFAULT_WINDOW
from .ui.app import AppController

LOGGER = logging.getLogger("spectrogram_viz")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="spectrogram-viz", description="Real-time FFT spectrum visualizer")
    p.add_argument("--device", type=int, default=None, help="Input device index")
    p.add_argument("--sample-rate", type=int, default=DEFAULT_SAMPLE_RATE)
    p.add_argument("--block-size", type=int, default=DEFAULT_BLOCK_SIZE)
    p.add_argument("--fft-size", type=int, default=DEFAULT_FFT_SIZE)
    p.add_argument("--window", type=str, default=DEFAULT_WINDOW, choices=("hann", "hamming", "blackman", "rect"))
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def configure_logging(verbosity: int) -> None:
    level = logging.WARNING if verbosity == 0 else (logging.INFO if verbosity == 1 else logging.DEBUG)
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def main(argv: list[str] | None = None) -> int:
    print("[DEBUG] cli.main: start")
    args = parse_args(argv)
    configure_logging(args.verbose)
    config = AudioConfig(
        sample_rate=args.sample_rate,
        block_size=args.block_size,
        fft_size=args.fft_size,
        window=args.window,
        device_index=args.device,
    )
    print(f"[DEBUG] cli.main: config={config}")
    return AppController(config).run()


if __name__ == "__main__":
    sys.exit(main())
