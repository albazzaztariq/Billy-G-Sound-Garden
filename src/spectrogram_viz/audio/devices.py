from dataclasses import dataclass
import logging
import sounddevice as sd
from ..errors import DeviceNotFoundError, SampleRateMismatchError

LOGGER = logging.getLogger(__name__)


@dataclass
class DeviceInfo:
    index: int
    name: str
    max_input_channels: int
    default_sample_rate: float
    hostapi: str


class DeviceManager:
    def list_input_devices(self) -> list[DeviceInfo]:
        out: list[DeviceInfo] = []
        hostapis = sd.query_hostapis()
        for idx, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                out.append(
                    DeviceInfo(
                        index=idx,
                        name=dev["name"],
                        max_input_channels=dev["max_input_channels"],
                        default_sample_rate=dev["default_samplerate"],
                        hostapi=hostapis[dev["hostapi"]]["name"],
                    )
                )
        return out

    def get_default_input(self) -> DeviceInfo:
        default_idx = sd.default.device[0]
        if default_idx is None or default_idx < 0:
            inputs = self.list_input_devices()
            if not inputs:
                raise DeviceNotFoundError("No input devices found")
            return inputs[0]
        dev = sd.query_devices(default_idx)
        return DeviceInfo(
            index=default_idx,
            name=dev["name"],
            max_input_channels=dev["max_input_channels"],
            default_sample_rate=dev["default_samplerate"],
            hostapi=sd.query_hostapis()[dev["hostapi"]]["name"],
        )

    def validate_device(self, index: int, sample_rate: int) -> None:
        try:
            dev = sd.query_devices(index)
        except (ValueError, sd.PortAudioError) as e:
            raise DeviceNotFoundError(f"Device index {index} not found") from e
        if dev["max_input_channels"] <= 0:
            raise DeviceNotFoundError(f"Device {index} has no input channels")
        try:
            sd.check_input_settings(device=index, samplerate=sample_rate)
        except sd.PortAudioError as e:
            raise SampleRateMismatchError(
                f"Device {index} does not support {sample_rate} Hz"
            ) from e
