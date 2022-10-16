import numpy as np
from DataClass import dataSpec
from DataClass import getScanNames

from matplotlib.widgets import MultiCursor
import matplotlib.pyplot as plt
from matplotlib.backend_tools import Cursors


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import platform,os

    if platform.system()== 'Windows':
        DirPath = os.getcwd()+"/data/"
    else:
        DirPath = '~/Documents/GinaSpectrum/'

    ScanList = getScanNames(DirPath)
    a = dataSpec(DirPath, ScanList[0])
    a.update()

#    ScanList=getScanNames('~/Documents/GinaSpectrum/')
#    ScanData,resultSpectra=getSpectras('~/Documents/GinaSpectrum/',ScanList[0])
#    dataset=pandas.read_csv('~/Documents/GinaSpectrum/Spectrum_86352.dat',sep='\t')
#    dataset2 = np.loadtxt('/home/nsluser/Documents/GinaSpectrum/Spectrum_86352_0.sub')
#    plt.imshow(np.log10(resultSpectra[30]))
#   plt.show()





fig, axs = plt.subplots(len(Cursors), figsize=(6, len(Cursors) + 0.5),
                        gridspec_kw={'hspace': 0})
fig.suptitle('Hover over an Axes to see alternate Cursors')

for cursor, ax in zip(Cursors, axs):
    ax.cursor_to_use = cursor
    ax.text(0.5, 0.5, cursor.name,
            horizontalalignment='center', verticalalignment='center')
    ax.set(xticks=[], yticks=[])


def hover(event):
    if fig.canvas.widgetlock.locked():
        # Don't do anything if the zoom/pan tools have been enabled.
        return

    fig.canvas.set_cursor(
        event.inaxes.cursor_to_use if event.inaxes else Cursors.POINTER)


fig.canvas.mpl_connect('motion_notify_event', hover)

plt.show()