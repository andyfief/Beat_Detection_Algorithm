# Beat Detection Algorithm
This project provides an algorithm to detect beats in an audio file. It uses Librosa for audio processing, NumPy for numerical operations, and Matplotlib for visualizations.

## How it works
Firstly, Librosa loads the audio file and returns a NumPy array of floating point values between -1 and 1 that represent the amplitude of the audio signal at every sample. Variable "samplerate" determines how many samples Librosa returns for each second of the input audio.
Using the default sample rate of 22050, a 3 minute song will return an array of length 3969000.

Next, we set a threshold to clip any values below a certain level. This helps to focus on the significant components of the audio while disregarding quieter noise or unwanted fluctuations. Additionally, any negative values are removed, ensuring the waveform 
consists only of non-negative amplitudes.

Next, we set two additional parameters:
  - chunk_size determines the number of indices that will be summed and added to a new array with size original_array/chunk_size.
  - min_distance determines the minimum distance between chunks that a new peak can be detected.

We then take the average amplitude within each chunk of our original array and add it to our new, smaller array.
This chunked data works better for peak detection because it removes the vast majority of the oscillations within the data. Audio waveforms are symmetric in nature, and millions of oscillations likely exist depending on the length of the input. 
Every index within a climb to a beat's true maximum has a corresponding index with a negative value (set to 0 after our thresholding). Chunking the data and averaging the values over a given time frame allows us to see a "higher-level" version of our data, effectively blurring
out the minute oscillations between relevant peaks.

Finally, we create a third array to store the indices of detected peaks and loop through our chunked array checking for local maxima at each position. We start at the second index and end at the second to last index because the edges of our array don't have two neighbors to
compare against. To find a local maxima, we simply check if an index has a greater value than both of its neighbors.

If a local maxima is found, we then check if the distance between the last detected peak and the current peak are greater than our specified distance. If this condition is met, the peak is added to our peak indices array.
The distance parameter is important because of the large number of oscillations in any audio waveform, mentioned previously. Even after chunking our data, there are still smaller oscillations present that we want to skip. Setting a minimum distance between beats ensures that
we only detect relevant peaks.

Chunk size and minimum distance should be adjusted to fit the needs of your audio file. Inputs with lower BPM can benefit from a higher minimum distance. Inputs with frequently changing amplitudes will benefit from a lower chunk size.
  - Minimum distance: Think about how often beats likely happen.
  - Chunk size: Think about how long a single beat lasts.

## Using Spleeter or Other Source Separation Methods
To isolate beats of a specific instrument, source separation libraries such as Spleeter can be used. Spleeter is a Python3.8 library that separates an audio file into 2-5 stems representing individual instruments present in the original audio. Using one of these
stem files as an input to this algorithm can yield excellent results.
