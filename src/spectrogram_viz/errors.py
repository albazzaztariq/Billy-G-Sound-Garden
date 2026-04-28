class SpectrogramVizError(Exception):
    pass

class SampleRateMismatchError(SpectrogramVizError):
    pass

class DeviceLostError(SpectrogramVizError):
    pass

class DeviceNotFoundError(SpectrogramVizError):
    pass

class BufferOverrunError(SpectrogramVizError):
    pass

class InvalidFFTSizeError(SpectrogramVizError):
    pass
