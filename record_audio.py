import sounddevice as sd
from scipy.io.wavfile import write
import os
from dotenv import load_dotenv

load_dotenv()

class AudioRecorder:
    def __init__(self):
        self.sample_rate = int(os.getenv('SAMPLE_RATE', 44100))
        # Check available devices and their channel counts
        self.devices = sd.query_devices()
        # Get default input device
        self.default_device = sd.query_devices(kind='input')
        # Use the channel count from the default device, fallback to 1 (mono) if issues occur
        self.channels = min(self.default_device['max_input_channels'], 1)

    def get_audio(self, filename, duration):
        print(f"Recording with {self.channels} channel(s)...")
        try:
            recording = sd.rec(int(duration * self.sample_rate), 
                               samplerate=self.sample_rate, 
                               channels=self.channels, 
                               dtype='int16')
            sd.wait()  # Wait until the recording is finished
            write(filename, self.sample_rate, recording)
            print(f"Recording finished. Saved as {filename}.")
        except Exception as e:
            print(f"Error during recording: {str(e)}")
            # Try with mono as fallback if there was an error
            if self.channels != 1:
                print("Trying with mono recording instead...")
                self.channels = 1
                self.get_audio(filename, duration)