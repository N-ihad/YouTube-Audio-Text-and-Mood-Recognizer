import os
from pydub import silence, AudioSegment
from EmptyFolder import emptyFolder

MIN_SILENCE_LEN = 300
MIN_DURATION = 2000
DEBUG = 0


def read_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1)

    return audio


def concatenate_edges(raw_interval):
    edges = [raw_interval[0]]

    # concatenate two edges if the interval btw them is too short
    for idx in range(1, len(raw_interval) - 1):
        cur_start = raw_interval[idx][0]
        prev_end = edges[-1][1]

        if cur_start - prev_end < MIN_SILENCE_LEN:
            edges[-1][1] = raw_interval[idx][1]
        else:
            edges.append(raw_interval[idx])

    return edges


def get_rid_of_short_intervals(edges):
    intervals = []

    for idx in range(len(edges)):
        if edges[idx][1]-edges[idx][0] > MIN_DURATION:
            intervals.append(edges[idx])

    return intervals


def splitAudioBySilence(audio_path, skip_idx=0, out_ext="wav", silence_thresh=-40, silence_chunk_len=100, keep_silence=100):
    audio = read_audio(audio_path)

    not_silence_ranges = silence.detect_nonsilent(
        audio, min_silence_len=silence_chunk_len,
        silence_thresh=silence_thresh)

    edges = concatenate_edges(not_silence_ranges)
    intervals = get_rid_of_short_intervals(edges)

    for idx, (start_idx, end_idx) in enumerate(intervals[skip_idx:]):
        start_idx = max(0, start_idx - keep_silence)
        end_idx += keep_silence
        
        segment = audio[start_idx:end_idx]
        segment.export("./chunks/chunk{0}.mp3".format(idx), out_ext)
        segment.set_channels(1)
        segment.export("./chunks/chunk{0}.wav".format(idx), format="wav")
        os.remove("./chunks/chunk{0}.mp3".format(idx))


# emptyFolder("./chunks/")
# splitAudioBySilence("audio.mp3")