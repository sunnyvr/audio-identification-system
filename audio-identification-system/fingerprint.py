import os
import librosa
import numpy as np
import scipy.ndimage as ndimage
from pick import savepickle
from matplotlib import pyplot as plt
from skimage.morphology import disk, diamond, square
from tqdm.auto import tqdm



class fingerprintBuilder:
    def __init__(self, dataPath, indexfile,
                spectype='stft', n_fft=1024, window='hann', win_length=1024, hop_length=512,
                shape='disk', neighbourhood=10, uniform=True, show=False,
                gap=50, targetsize=(200, 200)):

        #Spectogram Parameters
        self.spectype = spectype
        self.n_fft = n_fft
        self.window = window
        self.win_length = win_length
        self.hop_length = hop_length

        #Peak Picking Paramters
        self.shape = shape
        self.neighbourhood = neighbourhood
        self.uniform = uniform
        self.show = show

        #Combinatorial Parameters
        self.gap = gap
        self.targetsize = targetsize

        #Storing data
        self.data = {}
        self.title = []

        #Going through folder of .wav files
        for identity, filename in enumerate(tqdm(os.listdir(dataPath))):
            self.title.append(filename)
            hash_dict = self.fingerprint(dataPath+'/'+filename, identity)
            self.data.update(hash_dict)

        save_pickle(self, indexfile)


    def fingerprint(self, audio_file, identity=None):
        
        x, sr = librosa.load(os.path.join(audio_file)) #Loading the spectogram

        if self.spectype == 'stft':
            D = np.abs(librosa.stft(x, self.n_fft, self.hop_length, self.win_length, self.window))
        elif self.spectype == 'mel':
            D = librosa.feature.melspectrogram(x, sr, n_fft=self.n_fft, hop_length=self.hop_length, win_length=self.win_length, window=self.window)
        elif self.spectype == 'cqt':
            D = np.abs(librosa.cqt(x, sr, self.hop_length, window=self.window))

        peaks = self.pick_peaks(D)
        hdict = self.hash_peaks(peaks, identity)
        
        return hdict



    def pick_peaks(self, D):        #Peak picking

        assert self.shape == 'square' or self.shape == 'diamond' or self.shape == 'disk',\
        'Parameter shape must be set to \'disk\', \'diamond\' or \'square\''

        #Constellation Map generation
        data = np.log(D)
        footprint = eval(self.shape + '(' + str(self.neighbourhood) + ')')
        max_blobs = ndimage.maximum_filter(data, footprint=footprint)
        c_map = data == max_blobs


        if self.uniform:
            stdev = np.std(max_blobs)
            mean = np.mean(max_blobs)
            dist = np.multiply(data >= (mean-stdev), data <= (mean+stdev))
            c_map = np.multiply(c_map, dist)

        if self.show:
            plt.figure(figsize=(20, 5))
            plt.title('Spectrogram')
            plt.xlabel('Frames')
            plt.ylabel('Frequency bins')
            plt.imshow(librosa.amplitude_to_db(D,ref=np.max), origin='lower', cmap='reds')

            plt.figure(figsize=(20, 5))
            plt.title('Max Blobs')
            plt.xlabel('Frames')
            plt.ylabel('Frequency bins')
            plt.imshow(max_blobs, origin='lower', cmap='reds')

            plt.figure(figsize=(20, 5))
            plt.title('Constellaiton Map')
            plt.xlabel('Frames')
            plt.ylabel('Frequency bins')
            plt.imshow(c_map, origin='lower', cmap='reds')

        yfreq, xtime = np.nonzero(c_map)
        coordinates = list(zip(yfreq, xtime))

        coordinates = sorted(coordinates , key=lambda p: [p[1], p[0]])

        return coordinates  #Getting coordinate information



    def hash_peaks(self, peaks, identity=None):

        e = {}

        for anchorpts in peaks:

            freqstart = anchorpts[0] - (self.targetsize[0]//2)
            freqend = anchorpts[0] + (self.targetsize[0]//2)
            timestart = anchorpts[1] + self.gap
            timeend = timestart + self.targetsize[1]

            for target in peaks:

                if target[0] >= freqstart and target[0] <= freqend \
                    and target[1] >= timestart and target[1] <= timeend:

                    tdiff = target[1] - anchorpts[1]
                    key = str(anchorpts[0]) + str(target[0]) + str(tdiff)
                    if identity is not None: e[key] = (anchorpts[1], identity)
                    else: e[key] = anchorpts[1]

        return e

