import scipy
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import librosa
import soundfile

class sound():
    def __init__(self, name):
        self.data, self.rate = soundfile.read(name)

    def resample(self,data,rate,fs):
        re_data = librosa.resample(data,rate,fs)
        return re_data
    def filter(self, data,step, rate, fs1, fs2 = None, mode = 'lowpass'):
        if(mode == 'lowpass'):
            b, a = signal.butter(step, fs1 * 2 / rate, 'lowpass')
        elif(mode == 'highpass'):
            b, a = signal.butter(step, fs1 * 2 / rate, 'highpass')
        elif(mode == 'bandpass'):
            b, a = signal.butter(step, [fs1*2/rate, fs2*2/rate], 'bandpass')
        filt_data = signal.filtfilt(b, a, data)
        return filt_data
    def amplified(self, data,times):
        a_data = data * times
        return a_data
    def save(self, data , rate, name):
        soundfile.write(name, data, rate, subtype='PCM_24')

class spectrum():
    def __init__(self, name=None, data = None, rate = None):
        if(name != None):
            self.data , self.rate = soundfile.read(name)
        else:
            self.data = data
            self.rate = rate
        self.fig = None
    def draw_spc(self,data = None, nfft =1024, ylim = None,clim = None,show=False):
        cm = plt.cm.get_cmap('jet')
        if(data != None):
            plt.specgram(data, NFFT=nfft, Fs=self.rate, cmap=cm)
        else:
            plt.specgram(self.data, NFFT = nfft, Fs=self.rate, cmap=cm)
        plt.colorbar()
        if(ylim!=None):
            plt.ylim(ylim)
        if(clim!=None):
            plt.clim(clim)
        if(show):
            plt.show()
        self.fig = plt.gcf()
        plt.close()
    def save(self, name, dpi = 100):
        self.fig.savefig(name,dpi=dpi)
