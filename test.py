from tools import *
import soundfile
import librosa
import matplotlib.pyplot as plt
import antropy as ent
import librosa.display
import time
import os
'''f = open('C:/Users/yoyojoejoe/Desktop/test/list.txt', 'r')
for name in f.readlines():
    print(name)
    name1 = name.replace('\n','')

    name = 'C:/Users/yoyojoejoe/Desktop/test/resample32k/' + name1
    name1 = name1.replace('.wav', '')
    s = sound(name)
    for i in range(120):
        s1 = spectrum(data=s.data[(i) * 60 * s.rate:(i+1) * 60 * s.rate], rate=s.rate)
        s1.draw_spc(clim=[-50, -20],ylim=[0,8000],nfft = 2048)
        loc = 'C:/Users/yoyojoejoe/Desktop/test/resample32k/pic_1min/' + name1+ '_' + str(i) + ' - ' + str(i+1) + '.jpg'
        print(loc)
        s1.save(name=loc, dpi = 1000)
'''

time = 0
f = open('C:/Users/yoyojoejoe/Desktop/test/list.txt', 'r')
for ff in f.readlines():
    if (time%2==1):
        name1 = ff.replace('\n', '')
        name = 'D:/taichung/resample32k/' + name1
        name2 = name1.replace('.wav', '')
        os.mkdir('D:/taichung/result/'+ name2)
        s = sound(name = name)
        s.data = s.data * 5
        for i in range(120):
            data = s.data[(i) * 60 * s.rate:int((i+1) * 60 * s.rate)]
            data2 = data
            data = s.filter(data=data, step=4, rate=s.rate, fs1=400, fs2=5000, mode='bandpass')

            ll = []
            start = []
            end = []
            for j in range(60):
                aa = data[int(j*s.rate):int((j+1)*s.rate)]
                x = ent.spectral_entropy(aa, sf=s.rate, method='fft',normalize=True)
                ll.append(x)
            cheack = False
            for j in range(60):
                if (ll[j] <= (np.mean(ll) * 0.95)and cheack == False):
                    if(j==59):
                        end.append(j)
                    start.append(j)
                    cheack = True
                elif(ll[j] > (np.mean(ll) * 0.95) and cheack == True):
                    end.append(j)
                    cheack = False
                elif(j == 59 and cheack == True):
                    end.append(59)
            if (start):
                cheack = True
                for j in range(len(start)):
                    if(start[j]!=0 and end[j]!=59):
                        r = data[int((start[j]-1) * s.rate):int((end[j]+1) * s.rate)]
                        ss = data2[int((start[j]-1) * s.rate):int((end[j]+1) * s.rate)]
                    else:
                        r = data[int((start[j]) * s.rate):int((end[j]) * s.rate)]
                        ss = data2[int((start[j]) * s.rate):int((end[j]) * s.rate)]
                        cheack = False
                    if(cheack):
                        namm = 'D:/taichung/result/'+ name2+ '/' + str(i) + 'min' + str(
                            int(start[j])-1) + '-' + str(int(end[j])+1)
                    else:
                        namm = 'D:/taichung/result/'+ name2+ '/' + str(i) + 'min' + str(
                            int(start[j])) + '-' + str(int(end[j]))
                    if(start[j]!=end[j]):
                        namew = namm + '.wav'
                        namej = namm + '.jpg'
                        namea = namm + '-a' + '.jpg'
                        s.save(data=r, rate=s.rate, name=namew)
                        s1 = spectrum(data=r, rate=s.rate)
                        s1.draw_spc(nfft=2048, ylim=[0, 8000], clim=[-50, -15])
                        s1.save(namej, dpi=1000)
                        s2 = spectrum(data=ss, rate=s.rate)
                        s2.draw_spc(nfft=2048, ylim=[0, 8000], clim=[-50, -15])
                        s2.save(namea, dpi=1000)
    time = time + 1

# f = open('C:/Users/yoyojoejoe/Desktop/test/list1.txt', 'r')
# i = 0
# for ff in f.readlines():
#     if(i%2 == 1):
#         print(ff)
#         ff = ff.replace('\n', '')
#         s = sound(name = 'E:/台中0225_0304/un_近/' + ff)
#         r_data = s.resample(s.data,s.rate,32000)
#         r_data = s.amplified(r_data,100)
#         s.save(r_data,32000,'C:/Users/yoyojoejoe/Desktop/test/resample32k/' + ff)
#     i = i + 1
