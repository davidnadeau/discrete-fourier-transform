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

if __name__ == "__main__":
    w1 = readfile("w1.txt")
    w2 = readfile("w2.txt")
    print(foldwaves([w1,w2]))
