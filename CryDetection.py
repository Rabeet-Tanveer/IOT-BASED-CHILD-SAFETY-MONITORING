import numpy as np
import tensorflow as tf
import soundfile as sf
from python_speech_features import mfcc
import pyaudio
import wave
import sys

# Redirect stderr to /dev/null to suppress warnings
sys.stderr = open('/dev/null', 'w')

# Load the TensorFlow Lite model
model_path = 'Models/model11.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def record_audio(filename, duration=5, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100):
    p = pyaudio.PyAudio()

    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []
    for _ in range(int(rate / chunk * duration)):
        frames.append(stream.read(chunk))

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def extract_sampling_rate(audio_file):
    with sf.SoundFile(audio_file) as f:
        rate = f.samplerate
    return rate

def extract_mfcc_features(audio_file):
    signal, rate = sf.read(audio_file)
    segments = np.array_split(signal, 64)

    mfcc_features = []
    for segment in segments:
        features = mfcc(segment, rate, numcep=12, nfft=2048)
        mfcc_features.append(np.mean(features, axis=0))

    return np.array(mfcc_features).astype(np.float32)

def detect_baby_cry(audio_file):
    try:
        # Extract audio features
        features = extract_mfcc_features(audio_file)
        features = np.expand_dims(features, axis=0)
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], features)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])
        is_crying = int(output >= 0.6)
        return is_crying

    except KeyboardInterrupt:
        pass

