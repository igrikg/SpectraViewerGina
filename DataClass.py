import pandas
import glob
import numpy as np
import numpy.typing as npt
from os.path import expanduser, normpath, basename
from copy import copy


class DataArray:
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

    def recalculation_xy(self, XrecValue=None, YrecValue=None):

        if XrecValue is None:
            self.X = copy(self.X_old)
        else:
            self.X_old = copy(self.X)
            self.X = self.X*XrecValue
        if YrecValue is None:
            self.Y = copy(self.Y_old)
        else:
            self.Y_old = copy(self.Y)
            self.Y = self.Y * YrecValue

        self.Xminmax = (self.X.min(), self.X.max())
        self.Yminmax = (self.Y.min(), self.Y.max())
        self.Zminmax = (self.Z.min(), self.Z.max())
        self.Xslice = (self.X[0], np.sum(self.Z, 0))
        self.Yslice = (self.Y.transpose()[0], np.sum(self.Z, 1))


class DataSpec:
    '''
        dir_path - path to spectrrum folder
        scan_name - file name for *.dat file scan
    '''

    def __init__(self, dir_path: str, scan_name:str):
        self.list_spectrum = None
        self.scan_data = None
        self.result_spectra = None
        self.dir_path = dir_path
        self.scan_name = scan_name
        self.dir_path = self.dir_path.replace('~', expanduser('~'), 1)
        self.dir_path = normpath(self.dir_path)

        self.load_scan()
        self.load_spectrum()



    def load_scan(self):
        """Load Scan table"""
        self.scan_data = pandas.read_csv(self.dir_path + "\\" + self.scan_name + '.dat', sep='\t')



    def load_spectrum(self):
        """Load Spectrum"""
        self.scan_data = pandas.read_csv(self.dir_path + "\\" + self.scan_name + '.dat', sep='\t')
        self.list_spectrum = list(map(lambda x: basename(x), glob.glob(self.dir_path + "\\" + self.scan_name + '_*.sub')))
        self.list_spectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_') + 1:-4]))

        i = 0

        for spec_file in self.list_spectrum:
            array = np.loadtxt(self.dir_path + "\\" + spec_file).transpose()
            if not i:
                self.result_spectra = np.zeros((self.scan_data.values.shape[0], array.shape[0], array.shape[1]))
            if self.result_spectra[0].shape == array.shape:
                self.result_spectra[i] = array
                i += 1


    def update(self):
        """Load update scan table and add new spectrum"""
        shape = self.scan_data.values.shape
        self.load_scan()
        if shape != self.scan_data.values.shape and self.scan_data.values.shape[0] != 0:
            self.list_spectrum = list(map(lambda x: basename(x), glob.glob(self.dir_path + "\\" + self.scan_name + '_*.sub')))
            self.list_spectrum.sort(key=lambda elemStr: int(elemStr[elemStr.rfind('_') + 1:-4]))
            if self.result_spectra is None:
                i = 0
            else:
                i = self.result_spectra.shape[0]
            for specFile in self.list_spectrum:
                array = np.loadtxt(self.dir_path + specFile).transpose()
                if (not i): self.result_spectra = np.zeros(
                    (self.scan_data.values.shape[0], array.shape[0], array.shape[1]))
                self.result_spectra[i] = array
                i += 1
                
    def get_list_of_scan_colum(self):
        l=[self.scan_data.columns[0], self.scan_data.columns[-1]]
        if l[0]==l[1]:
            return [l[0]]
        else:
            return l

    def get_list_of_first_colum(self):
        return self.scan_data.loc[:, self.scan_data.columns[0]].to_list()

    def get_sum_result_spectra(self, listRange):
        return np.sum(np.sum(self.result_spectra[:, listRange[0]:listRange[1], listRange[2]:listRange[3]], axis=1), axis=1)

    def get_sum_plot(self, listRange):
        result=[]
        # divite if we have some polarising mode
        x_panda = self.scan_data.iloc[:, 0]
        x_uniq = x_panda.unique()
        numbers_of_spectra = x_panda.shape[0] // x_uniq.shape[0]

        for i in range(numbers_of_spectra):
            intensity = np.sum(
                np.sum(self.result_spectra[i::numbers_of_spectra, listRange[0]:listRange[1], listRange[2]:listRange[3]],
                    axis=1),
                     axis=1)
            angeles = x_uniq[0:intensity.shape[0]]
            result.append((angeles, intensity))
        return result




def get_scan_names(dir_path_scans: str):
        dir_path_scans: str = dir_path_scans.replace('~', os.path.expanduser('~'), 1)
        list_scans = list(
            map(lambda x: basename(x[:x.rfind('.')]), glob.glob(os.path.normpath(dir_path_scans + '/*.dat'))))
        return list_scans

if __name__ == '__main__':
    import platform, os
    if platform.system()== 'Windows':
        dir_path = os.getcwd() + "/data/"
    else:
        dir_path = '~/Documents/GinaSpectrum/'




    ScanList= get_scan_names(dir_path)
    a = DataSpec(dir_path, ScanList[7])
    print(a.get_sum_plot([10, 20, 30, 35]))
    a.update()