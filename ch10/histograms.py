'''

    GENERA Histogramma dei valori presenti in un raster

'''
import os
import gdal
import numpy as np
import matplotlib.pyplot as plt

os.chdir('../dati/osgeopy-data/Switzerland/')
DS = gdal.Open('dem_class2.tif')
BAND = DS.GetRasterBand(1)

APPROXIMATE_HIST = BAND.GetHistogram()
EXACT_HIST = BAND.GetHistogram(approx_ok=False)

n_groups = len(EXACT_HIST[:7])
arr = np.array([APPROXIMATE_HIST[1:6], EXACT_HIST[1:6]])

print('Approximate:', APPROXIMATE_HIST[:7], sum(APPROXIMATE_HIST))
print('Exact:', EXACT_HIST[:7], sum(EXACT_HIST))

print('Approximate 1-6:', APPROXIMATE_HIST[1:6])

fig, ax = plt.subplots()
index = np.arange(1, n_groups-1)
BAR_WIDTH = 0.35
OPACITY = 0.6
ERROR_CONFIG = {'ecolor': '0.3'}

rects1 = plt.bar(index, APPROXIMATE_HIST[1:6], BAR_WIDTH,
                 alpha=OPACITY,
                 color='b',
                 error_kw=ERROR_CONFIG,
                 yerr=arr[0]/2,
                 label='Approximate')

rects2 = plt.bar(index + BAR_WIDTH, EXACT_HIST[1:6], BAR_WIDTH,
                 alpha=OPACITY,
                 color='r',
                 error_kw=ERROR_CONFIG,
                 yerr=arr[1]/2,
                 label='Exact')

plt.xlabel('Classes')
plt.ylabel('Frequencies')
plt.title('Values grouped by exact and approximate image values')
plt.xticks(index + BAR_WIDTH, ('1', '2', '3', '4', '5'))
plt.legend()

plt.tight_layout()
plt.show()
