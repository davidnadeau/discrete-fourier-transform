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
    return samples

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

#add 2 waves, return single result wave
def addWaves(a, b, channels):
    return [[int (x[i]) + int (y[i]) for x, y in zip(a, b)] for i in range(channels)]

if __name__ == "__main__":
    w1 = readfile("w1.txt")
    w2 = readfile("w2.txt")
    sumWave = addWaves(w1, w2, 2)
    print(sumWave)
    #readfile("gipsy.kings.hotel.california.txt")
