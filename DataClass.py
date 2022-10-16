import pandas
import glob,os
import numpy as np


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



    def loadScan(self):
        '''Load Scan table'''
        self.ScanData = pandas.read_csv(self.DirPath +"\\"+ self.ScanName + '.dat', sep='\t')



    def loadSpectrum(self):
        '''Load Sspectrums'''
        self.ScanData = pandas.read_csv(self.DirPath +"\\"+ self.ScanName + '.dat', sep='\t')
        self.ListSpectrum = list(map(lambda x: os.path.basename(x), glob.glob(self.DirPath+"\\"+self.ScanName + '_*.sub')))
        self.ListSpectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_') + 1:-4]))
        i = 0

        for specFile in self.ListSpectrum:
            array = np.loadtxt(self.DirPath+"\\"+ specFile).transpose()
            if (not i): self.ResultSpectra = np.zeros((self.ScanData.values.shape[0], array.shape[0], array.shape[1]))
            self.ResultSpectra[i] = array
            i += 1



    def update(self):
        '''Load update scan table and add new spectrum'''
        shape = self.ScanData.values.shape
        self.loadScan()
        if shape != self.ScanData.values.shape and self.ScanData.values.shape[0] != 0:
            self.ListSpectrum = list(map(lambda x: os.path.basename(x), glob.glob(self.DirPath+"\\"+self.ScanName + '_*.sub')))
            self.ListSpectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_') + 1:-4]))
            if self.ResultSpectra is None:
                i = 0
            else:
                i = self.ResultSpectra.shape[0]
            for specFile in self.ListSpectrum:
                array = np.loadtxt(self.DirPath + specFile).transpose()
                if (not i): self.ResultSpectra = np.zeros(
                    (self.ScanData.values.shape[0], array.shape[0], array.shape[1]))
                self.ResultSpectra[i] = array
                i += 1
def getScanNames(dirPath):
    dirPath = dirPath.replace('~', os.path.expanduser('~'), 1)
    listScans = list(map(lambda x: os.path.basename(x[:x.rfind('.')]), glob.glob(os.path.normpath(dirPath+'/*.dat'))))

    return listScans

if __name__ == '__main__':
    import platform,os
    if platform.system()== 'Windows':
        DirPath = os.getcwd()+"/data/"
    else:
        DirPath = '~/Documents/GinaSpectrum/'

    ScanList = getScanNames(DirPath)
    a = dataSpec(DirPath, ScanList[0])
    a.update()