# from librosa examples, and modified by Steve Rubin - srubin@cs.berkeley.edu
import numpy as np
import scipy
import scipy.signal
import librosa


def structure(X):
    d, n = X.shape
    X = scipy.stats.zscore(X, axis=1)
    D = scipy.spatial.distance.squareform(
        scipy.spatial.distance.pdist(X.T, metric="cosine"))
    return D[:-1, :-1]


def analyze_file(infile, debug=False):
    y, sr = librosa.load(infile, sr=44100)
    return analyze_frames(y, sr, debug)


def analyze_frames(y, sr, debug=False):
    A = {}

    hop_length = 128

    # First, get the track duration
    A['duration'] = float(len(y)) / sr

    # Then, get the beats
    if debug: print "> beat tracking"
    tempo, beats = librosa.beat.beat_track(y, sr, hop_length=hop_length)

    # Push the last frame as a phantom beat
    A['tempo'] = tempo
    A['beats'] = librosa.frames_to_time(
        beats, sr, hop_length=hop_length).tolist()

    if debug: print "beats count: ", len(A['beats'])

    if debug: print "> spectrogram"
    S = librosa.feature.melspectrogram(y, sr,
                                       n_fft=2048,
                                       hop_length=hop_length,
                                       n_mels=80,
                                       fmax=8000)
    S = S / S.max()

    # A['spectrogram'] = librosa.logamplitude(librosa.feature.sync(S, beats)**2).T.tolist()

    # Let's make some beat-synchronous mfccs
    if debug: print "> mfcc"
    S = librosa.feature.mfcc(S=librosa.logamplitude(S), n_mfcc=40)
    A['timbres'] = librosa.feature.sync(S, beats).T.tolist()

    if debug: print "timbres count: ", len(A['timbres'])

    # And some chroma
    if debug: print "> chroma"
    S = np.abs(librosa.stft(y, hop_length=hop_length))

    # Grab the harmonic component
    H = librosa.decompose.hpss(S)[0]

    # H = librosa.hpss.hpss_median(S, win_P=31, win_H=31, p=1.0)[0]
    A['chroma'] = librosa.feature.sync(librosa.feature.chromagram(S=H, sr=sr),
                                        beats,
                                        aggregate=np.median).T.tolist()

    # Relative loudness
    S = S / S.max()
    S = S**2

    if debug: print "> dists"
    dists = structure(np.vstack([np.array(A['timbres']).T, np.array(A['chroma']).T]))
    A['dense_dist'] = dists

    edge_lens = [A["beats"][i] - A["beats"][i - 1]
                 for i in xrange(1, len(A["beats"]))]
    A["avg_beat_duration"] = np.mean(edge_lens)
    A["med_beat_duration"] = np.median(edge_lens)

    return A


if __name__ == '__main__':
    import sys
    from radiotool.composer import Song

    song = Song(sys.argv[1], cache_dir=None)
    frames = song.all_as_mono()
    analyze_frames(frames, song.samplerate)
