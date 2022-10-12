import os,pandas,glob
import numpy as np

def getScanNames(dirPath) :
    dirPath=dirPath.replace('~',os.path.expanduser('~'),1)
    listScans=list(map(lambda x: os.path.split(x[:x.rfind('.')])[1],glob.glob(os.path.normpath(dirPath+'/*.dat'))))
    return listScans

class dataSpec:
    '''
        dirPath - path to spectrrum folder
        ScanName - file name for *.dat file scan
    '''
    def __init__(self, DirPath, ScanName):
        self.DirPath=DirPath
        self.ScanName=ScanName
        self.DirPath = self.DirPath.replace('~', os.path.expanduser('~'), 1)
        self.DirPath = os.path.normpath(self.DirPath)
        self.ResultSpectra=None
        self.loadScan()
        self.loadSpectrum()
    '''Load Scan table'''
    def loadScan(self):
        self.ScanData = pandas.read_csv(self.DirPath +"\\"+ self.ScanName + '.dat', sep='\t')

    '''Load Sspectrums'''
    def loadSpectrum(self):
        self.ScanData = pandas.read_csv(self.DirPath +"\\"+ self.ScanName + '.dat', sep='\t')
        self.ListSpectrum = glob.glob(self.ScanName + '_*.sub', root_dir=self.DirPath)
        self.ListSpectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_') + 1:-4]))
        i = 0;

        for specFile in self.ListSpectrum:
            array = np.loadtxt(self.DirPath + specFile).transpose()
            if (not i): self.ResultSpectra = np.zeros((self.ScanData.values.shape[0], array.shape[0], array.shape[1]))
            self.ResultSpectra[i] = array
            i += 1

    '''Load update scan table and add new spectrum'''
    def update(self):
        shape = self.ScanData.values.shape
        self.loadScan()
        if shape != self.ScanData.values.shape and self.ScanData.values.shape[0] !=0:
            self.ListSpectrum = glob.glob(self.ScanName + '_*.sub', root_dir=dirPath)
            self.ListSpectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_') + 1:-4]))
            if self.ResultSpectra is None: i=0
            else: i=self.ResultSpectra.shape[0]
            for specFile in self.ListSpectrum:
                array = np.loadtxt(self.DirPath + specFile).transpose()
                if (not i): self.ResultSpectra = np.zeros(
                    (self.ScanData.values.shape[0], array.shape[0], array.shape[1]))
                self.ResultSpectra[i] = array
                i += 1

if __name__ == "__main__":
    pass