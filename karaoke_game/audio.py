import sounddevice as sd
import numpy as np

CHUNK_SIZE = 1024
RATE = 44100
CHANNELS = 1


class AudioInput:
    def __init__(self, device=None):
        self.device = device or self._select_device()
        self.buffer = np.zeros(CHUNK_SIZE)
        self._stream = sd.InputStream(
            device=self.device,
            channels=CHANNELS,
            samplerate=RATE,
            blocksize=CHUNK_SIZE,
            callback=self._callback,
            latency="low"
        )

    def _select_device(self):
        return 1 # hardcoded for testing, change to dynamic selection if needed
        print("Available input devices:\n")
        for i, dev in enumerate(sd.query_devices()):
            if dev['max_input_channels'] > 0:
                print(f"{i}: {dev['name']}")
        return int(input("\nSelect input device: "))

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.buffer = indata[:, 0].copy()

    def get_pitch(self):
        samples = self.buffer
        window = np.hanning(len(samples))  # create hanning window
        spectrum = np.abs(np.fft.rfft(samples * window))
        freqs = np.fft.rfftfreq(len(samples), d=1/RATE)

        mask = (freqs > 50) & (freqs < 2000)  # limit to vocal range
        peak_idx = np.argmax(spectrum[mask])  # find peak in spectrum
        pitch = freqs[mask][peak_idx]  # get pitch corresponding to peak
        return pitch

    # allows usage with "with" statement
    def __enter__(self):
        self._stream.start()

    def __exit__(self, *args):
        self._stream.stop()
        self._stream.close()