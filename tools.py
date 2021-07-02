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



def entropy(data,fs,weight=None,axis=-1,normalize=True):
    f, psd = signal.periodogram(data, fs, axis=-1)
    psd_norm = psd / psd.sum(axis=axis, keepdims=True)
    if(weight is None):
        weight = np.ones(np.size(psd_norm))
    else:
        weight=weight
    try:
        se = -(psd_norm * np.log2(psd_norm) * weight).sum(axis=axis)
    except:
        weight = np.ones(np.size(psd_norm))
        se = -(psd_norm * np.log2(psd_norm) * weight).sum(axis=axis)
    if normalize:
        se /= np.log2(psd_norm.shape[axis])
    return se

def get_weight(rate):
    weight = np.ones(int((rate / 2) + 1))
    for i in range(200, 400):
        weight[i] = 1.5
    for i in range(1500, 5000):
        weight[i] = 0.5
    return weight

def epd(name,wav_name,times):
    s = sound(name=name)
    s.data = s.amplified(s.data,500)
    s.data = s.data - np.mean(s.data)
    weight = np.ones(int((s.rate / 2) + 1))
    for i in range(120):
        data = s.data[(i) * 60 * s.rate:int((i + 1) * 60 * s.rate)]
        data2 = data
        data = s.filter(data=data,step=6,rate=s.rate,fs1=200,fs2=5000,mode='bandpass')
        ll = []
        start = []
        end = []
        for j in range(60):
            aa = data[int(j * s.rate):int((j + 1) * s.rate)]
            x = entropy(aa,s.rate,weight=weight)
            ll.append(x)
        cheack = False
        for j in range(60):
            if (ll[j] <= (np.nanmean(ll) * times) and cheack == False):
                if (j == 59):
                    end.append(j)
                start.append(j)
                cheack = True
            elif (ll[j] > (np.nanmean(ll) * times) and cheack == True):
                end.append(j)
                cheack = False
            elif (j == 59 and cheack == True):
                end.append(59)
        if (start):
            cheack = True
            for j in range(len(start)):
                if (start[j] != 0 and end[j] != 59):
                    r = data[int((start[j] - 1) * s.rate):int((end[j] + 1) * s.rate)]
                    ss = data2[int((start[j] - 1) * s.rate):int((end[j] + 1) * s.rate)]
                else:
                    r = data[int((start[j]) * s.rate):int((end[j]) * s.rate)]
                    ss = data2[int((start[j]) * s.rate):int((end[j]) * s.rate)]
                    cheack = False
                if (cheack):
                    namm = wav_name + '/' + str(i) + 'min' + str(
                        int(start[j]) - 1) + '-' + str(int(end[j]) + 1)
                else:
                    namm = wav_name + '/' + str(i) + 'min' + str(
                        int(start[j])) + '-' + str(int(end[j]))
                if (start[j] != end[j]):
                    namew = namm + '.wav'
                    namea = namm + '.jpg'
                    s.save(data=r, rate=s.rate, name=namew)
                    s2 = spectrum(data=ss, rate=s.rate)
                    s2.draw_spc(nfft=2048, ylim=[0, 8000], clim=[-55, -25])
                    s2.save(namea, dpi=1000)
