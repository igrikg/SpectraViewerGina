# This is a sample Python script.
import pandas
import numpy as np
import matplotlib.pyplot as plt
import os,glob
from dataclass import dataSpec
def getScanNames(dirPath) :
    dirPath=dirPath.replace('~',os.path.expanduser('~'),1);
    listScans=list(map(lambda x: x[:x.rfind('.')],glob.glob('*.dat',root_dir=dirPath)))
    return listScans


def getSpectras (dirPath,ScanName) :
    dirPath=dirPath.replace('~',os.path.expanduser('~'),1);
    ScanData = pandas.read_csv(dirPath+ScanName+'.dat', sep='\t')
    listSpectrum=glob.glob(ScanName+'_*.sub',root_dir=dirPath)
    listSpectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_')+1:-4]))
    i=0;
    for specFile in listSpectrum:
        array = np.loadtxt(dirPath+specFile).transpose()
        if (not i): resultSpectra=np.zeros((ScanData.values.shape[0],array.shape[0],array.shape[1]))
        resultSpectra[i]=array
        i+=1
    return ScanData,resultSpectra

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dirpath='~/Documents/GinaSpectrum/'
    ScanList = getScanNames(dirpath)
    a=dataSpec(dirpath,ScanList[0])
    a.update()

#    ScanList=getScanNames('~/Documents/GinaSpectrum/')
#    ScanData,resultSpectra=getSpectras('~/Documents/GinaSpectrum/',ScanList[0])
#    dataset=pandas.read_csv('~/Documents/GinaSpectrum/Spectrum_86352.dat',sep='\t')
#    dataset2 = np.loadtxt('/home/nsluser/Documents/GinaSpectrum/Spectrum_86352_0.sub')
#    plt.imshow(np.log10(resultSpectra[30]))
#   plt.show()






