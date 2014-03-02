#####################################
#Author:    David Nadeau            #
#Purpose:   recreate wave using DFT #
#####################################
import math
#####################################
#   READING FROM TEXT FILE          #
#####################################

def readfile(file):
    #open file
    txt = open(file, "r")
    #read header information
    header = readheader(txt)
    #read samples into array
    samples = readsamples(txt, header['samples'])
    #free file resource
    txt.close()
    #return samples
    return {
        "header": header,
        "samples": samples
    }

def readheader(txt):
    return {
        "samples":      int (readcolumn(txt, 1)),
        "bps":          int (readcolumn(txt, 1)),
        "channels":     int (readcolumn(txt, 1)),
        "samplerate":   int (readcolumn(txt, 1)),
        "normalized":   readcolumn(txt, 1)
    }    

#read a single column from a text file
def readcolumn(txt, i):
    return txt.readline().split()[i]

#read every sample, return 2d list [ [c1, c2], [c1,c2], ... ]
#where: 
#   [i][0] is the first channel of sample i
#   [i][1] is the second channel of sample i
def readsamples(txt, samples):
    return [readsample(txt) for x in range(samples)]

#read a line from the txt file, return array of words (split on whitespace)
def readsample(txt):
    return txt.readline().split()

#####################################
#   WRITE TO TEXT                   #
#####################################
def writewave(filename, w, wave):
    file = open(filename, 'w+')
    file.write(createheader(w))
    for i in range(w['header']['samples']):
        file.write(str(round(wave[i][0])))
        if w['header']['channels'] == 2:
           file.write('\t' + str(round(wave[i][1])) + '\n')
        else:
            file.write('\n')

def createheader(w):
    header =  "SAMPLES\t" + str(w['header']['samples']) + "\n"
    header += "BITSPERSAMPLE:\t"+ str(w['header']['bps']) + "\n"
    header += "CHANELS:\t"+ str(w['header']['channels']) + "\n" 
    header += "SAMPLERATE:\t"+ str(w['header']['samplerate']) + "\n"
    header += "NORMALIZED:\t"+ str(w['header']['normalized']) + "\n"
    return header 

#####################################
#   SUMMING WAVES                   #
#####################################

#add n waves
def foldwaves(waves, channels):
    origwave = []
    for w in waves:
        ch = []
        for c in range(channels):
            value = 0
            for s in w:
                value += s[c]['amplitude']
            ch.append(value)
        origwave.append(ch)
    return origwave 

#####################################
#   DISCRETE FOURIER TRANSFORM      #
#####################################
# t = time (from 0,...,T-1)
# T = total # samples
# f(t) is amplitude of wave at time t
# n = harmonic number (max possible harmonic is T/2, or Nyquist frequency)
# x[k] is sample at index k in wave table
#####################################

def reconstructdft(w, T, channels):
    return foldwaves(w, channels)

def deconstructdft(w, T, channels):
    waves = []
    for t in range(T):
        harmonics = []
        for n in range(1, round(T/2)):
            c = []
            for i in range(channels):
                anot = a0(T, w, i)
                an = getan(T, n, w, i)
                bn = getbn(T, n, w, i)
                p1 = an * math.cos((2*math.pi*n*t) / T)
                p2 = bn * math.sin((2*math.pi*n*t) / T)
                c.append({
                    "number": t,
                    "coefficients": {"a": an, "b": bn},
                    "amplitude": p1 + p2 + anot
                })
            harmonics.append(c)
        waves.append(harmonics) 
    return waves

def getan(T, n, x, channel):
    sum = 0;
    for i in range(T):
        sum += int(x[i][channel])* math.cos( (2*math.pi*n*i) / T )
    return sum * (2/T)

def getbn(T, n, x, channel):
    sum = 0;
    for i in range(T):
        sum += int(x[i][channel])* math.sin( (2*math.pi*n*i) / T )
    return sum * (2/T)

def a0(T, x, channel):
    sum = 0;
    for i in range(T):
        sum += int(x[i][channel])
    return sum * (1/T)

if __name__ == "__main__":
    w1 = readfile("w2.txt")
    print("Original wave:\n", w1['samples'], '\n')
    dftwaves = deconstructdft(w1['samples'], w1['header']['samples'], w1['header']['channels'])
    #print("DFT waves:\n", dftwaves, '\n')
    wave = reconstructdft(dftwaves, w1['header']['samples'], w1['header']['channels'])
    print("Reconstructed wave:\n", wave, '\n')
    writewave("tetwtwet", w1, wave)
