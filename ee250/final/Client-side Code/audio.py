# Audio application libraries:
import pyaudio
import wave
import os
import sys


window = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Currently Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=window,
                input=True)

frames = []  # Initialize array to store frames

# Store data in window for 3 seconds
for i in range(0, int(fs / window * seconds)):
    data = stream.read(window)
    frames.append(data)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Recording completed.')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()

text_file = open("target_note.txt", "w")
text_file.write(str(sys.argv[1]))
text_file.close()