from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def match_target_amplitude(aChunk, target_dBFS):
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def splitAudioBySilence(filename):
    song = AudioSegment.from_mp3(filename)
    chunks = split_on_silence (song, min_silence_len = 2000, silence_thresh = -19)

    for i, chunk in enumerate(chunks):
        silence_chunk = AudioSegment.silent(duration=500)
        audio_chunk = silence_chunk + chunk + silence_chunk
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
        print("Exporting chunk{0}.mp3.".format(i))
        normalized_chunk.export("./chunks/chunk{0}.mp3".format(i), bitrate = "192k", format = "mp3")
        sound = AudioSegment.from_mp3("./chunks/chunk{0}.mp3".format(i))
        sound = sound.set_channels(1)
        sound.export("./chunks/chunk{0}.wav".format(i), format="wav")
        os.remove("./chunks/chunk{0}.mp3".format(i))

# splitAudioBySilence("test.mp3")