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
#   SUMMING WAVES                   #
#####################################

#add n waves
def foldwaves(waves):
    #create empty wave to serve as an accumulator
    result = emptywave(waves[0]['header']['samples'], waves[0]['header']['channels'])
    for w in waves:
        result = addwaves(result, w['samples'], w['header']['samples'], w['header']['channels'])
    return result

#add 2 waves, return single result wave
def addwaves(a, b, samples, channels):
    return [[int(a[i][j]) + int(b[i][j]) for j in range(channels)] for i in range(samples)]

#create default empty wave for wave summation
def emptywave(samples, channels):
    return [[0 for i in range(channels)] for j in range(samples)]

#####################################
#   DISCRETE FOURIER TRANSFORM      #
#####################################
# t = time (from 0,...,T-1)
# T = total # samples
# f(t) is amplitude of wave at time t
# n = harmonic number (max possible harmonic is T/2, or Nyquist frequency)
# x[k] is sample at index k in wave table
#####################################

def reconstructdft(w):
    T = w['header']['samples']
    for t in range(T):
        print(t,":\t",w['samples'][t][0], '\t',deconstructdft(w, t)) 

def deconstructdft(w, t):
    T = w['header']['samples']
    x = w['samples']
    sum = 0

    for n in range(1, round(T/2)):
        p1 = an(T, n, x) * math.cos((2*math.pi*n*t) / T)
        p2 = bn(T, n, x) * math.sin((2*math.pi*n*t) / T)
        sum += p1 + p2 + a0(T, x)
    
    return sum 

def an(T, n, x):
    sum = 0;
    for i in range(T):
        sum += int(x[i][0])* math.cos( (2*math.pi*n*i) / T )
    return sum * (2/T)

def bn(T, n, x):
    sum = 0;
    for i in range(T):
        sum += int(x[i][0])* math.sin( (2*math.pi*n*i) / T )
    return sum * (2/T)

def a0(T, x):
    sum = 0;
    for i in range(T):
        sum += int(x[i][0])
    return sum * (1/T)

if __name__ == "__main__":
    w1 = readfile("w1.txt")
    #w2 = readfile("w2.txt")
    #print(foldwaves([w1,w2]))
    reconstructdft(w1)
