import librosa
import numpy as np
import matplotlib.pyplot as plt

def load_song(file):
    y, sr = librosa.load(file)
    return y, sr

def remove_negatives(data):
    return np.maximum(data, 0)

def clip_threshold(data, threshold):
    return np.maximum(data, threshold)

def find_peaks(data, distance):
    peak_idxs = []
    
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            if len(peak_idxs) == 0 or i - peak_idxs[-1] >= distance:
                peak_idxs.append(i)
    print(len(peak_idxs))
    return peak_idxs

def get_sample(start_time, end_time, samplerate):
    start_sample = int(start_time * samplerate)
    end_sample = int(end_time * samplerate)
    return start_sample, end_sample

def display_wave(data, samplerate, start_sample, end_sample):
    segment = data[start_sample:end_sample]
    time = np.arange(len(segment)) / samplerate

    plt.figure(figsize=(15, 6))
    plt.plot(time, segment, label="Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Waveform Display")
    plt.legend()
    plt.grid()

def display_peaks(peaks, threshold, start_time, start_sample, end_sample, samplerate, chunk_size, min_distance):
    scaled_peaks = [peak * chunk_size for peak in peaks]
    filtered_peaks = [peak for peak in scaled_peaks if start_sample <= peak < end_sample]

    plt.axhline(y=threshold, color='g', linestyle='-', alpha=0.8, label='Threshold')
    last_peak_time = None
    for peak in filtered_peaks:
        time = peak / samplerate
        if last_peak_time is None or (time - last_peak_time) >= min_distance:
            plt.axvline(x=time - start_time, color='r', linestyle='-', alpha=0.8, label='Peak')
            last_peak_time = time

def get_tempo_frames(data, samplerate):
    tempo, beat_frames = librosa.beat.beat_track(y=data, sr=samplerate)
    return tempo, beat_frames

def get_beattimes(frames, samplerate):
    beat_times = librosa.frames_to_time(frames, sr=samplerate)
    return beat_times

def chunk_data(data, chunk_size, threshold)
    data = clip_threshold(data, threshold)

    abs_data = np.abs(data)

    num_chunks = len(abs_data) // chunk_size
    chunked_values = []

    for i in range(num_chunks):
        chunk = abs_data[i * chunk_size:(i + 1) * chunk_size]
        chunk_sum = np.sum(chunk) / chunk_size
        chunked_values.append(chunk_sum)

    return np.array(chunked_values)

if __name__ == '__main__':
    file = "../spleet/output/where-the-wild-things-are/drums.wav"
    data, samplerate = load_song(file)

    start_time = 0
    end_time = 299
    start_sample, end_sample = get_sample(start_time, end_time, samplerate)

    data = remove_negatives(data)

    display_wave(data, samplerate, start_sample, end_sample)

    chunk_size = 25
    threshold = 0.4
    min_distance = 0.1

    chunked_data = chunk_data(data, chunk_size, threshold)

    distance = 10
    peaks = find_peaks(chunked_data, distance)

    display_peaks(peaks, threshold, start_time, start_sample, end_sample, samplerate, chunk_size, min_distance)
    plt.show()
