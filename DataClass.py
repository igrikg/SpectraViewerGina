import pandas
import glob,os
import numpy as np
import numpy.typing as npt
from copy import copy

class DataArray():
    def __init__(self, data: npt.NDArray,X=None,Y=None):
        self.Z=data
        if X is None: X = np.arange(-self.Z.shape[0]/2, self.Z.shape[0]/2, 1)
        if Y is None: Y = np.arange(-self.Z.shape[1]/2, self.Z.shape[1]/2, 1)
        self.X, self.Y = np.meshgrid(X, Y)
        self.X_old = copy(self.X)
        self.Y_old = copy(self.Y)
        self.shape = data.shape
        self.Xminmax = (self.X.min(), self.X.max())
        self.Yminmax = (self.Y.min(), self.Y.max())
        self.Zminmax = (self.Z.min(), self.Z.max())
        self.Xslice=(X,np.sum(self.Z,0))
        self.Yslice=(Y,np.sum(self.Z,1))

    def recalculationXY(self,XrecValue=None,YrecValue=None):
        if XrecValue==None:
            self.X = copy(self.X_old)
        else:
            self.X_old = copy(self.X)
            self.X = self.X*XrecValue
        if YrecValue==None:
            self.Y = copy(self.Y_old)
        else:
            self.Y_old = copy(self.Y)
            self.Y = self.Y * YrecValue
        self.Xminmax = (self.X.min(), self.X.max())
        self.Yminmax = (self.Y.min(), self.Y.max())
        self.Zminmax = (self.Z.min(), self.Z.max())
        self.Xslice = (self.X[0], np.sum(self.Z, 0))
        self.Yslice = (self.Y.transpose()[0], np.sum(self.Z, 1))


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
            if self.ResultSpectra[0].shape == array.shape:
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
    def getListOfScanColums(self):
        l=[self.ScanData.columns[0],self.ScanData.columns[-1]]
        if l[0]==l[1]:
            return [l[0]]
        else:
            return l

    def getListOfFirstColums(self):
        return self.ScanData.loc[:,self.ScanData.columns[0]].to_list()

    def getSumResultSpectra(self,listRange):
        return np.sum(np.sum(self.ResultSpectra[:,listRange[0]:listRange[1],listRange[2]:listRange[3]], axis=1), axis=1)

    def getSumPlot(self, listRange):
        result=[]
        x_panda = self.ScanData.iloc[:, 0]
        x_uniq = x_panda.unique()

        numberOfSpectras=x_panda.shape[0]//x_uniq.shape[0]
        #print(x_uniq.shape)
        #print(x.shape)
        for i in range(numberOfSpectras):
            Y=np.sum(np.sum(self.ResultSpectra[i::numberOfSpectras, listRange[0]:listRange[1], listRange[2]:listRange[3]], axis=1), axis=1)
            X=x_uniq[0:Y.shape[0]]
            result.append((X, Y))
        return result



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
    a = dataSpec(DirPath, ScanList[7])
    print(a.getSumPlot([10,20,30,35]))
    a.update()