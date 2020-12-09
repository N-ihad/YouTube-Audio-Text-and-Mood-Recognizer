import pyaudio
import os
import wave
import pickle
import soundfile
import numpy as np
from pydub import AudioSegment
import librosa
from sys import byteorder
from array import array
from struct import pack
from sklearn.neural_network import MLPClassifier

# from utils import extract_feature

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 16000

SILENCE = 30

def extract_feature(file_name, **kwargs):
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result = np.hstack((result, mel))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
            result = np.hstack((result, tonnetz))
    return result

def recognizeEmotion():
    model = pickle.load(open("result/mlp_classifier.model", "rb"))
    for filename in os.listdir("./chunks/"):
        if filename.endswith(".wav"): 
            features = extract_feature("./chunks/" + filename, mfcc=True, chroma=True, mel=True).reshape(1, -1)
            result = model.predict(features)[0]
            f = open("./emotions/" + filename[:-4] + "_emotion" + ".txt", "w+")
            f.write(result)
            f.close()
            continue
        else:
            print("entered4")
            continue


# recognizeEmotion("chunk1.mp3")