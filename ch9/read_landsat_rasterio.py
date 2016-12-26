import os
import rasterio
from matplotlib import pyplot

os.chdir(r'C:\Users\Fabio\Documents\Programmazione\PycharmProjects\geoprocessing\dati\osgeopy-data\Landsat\Washington')
src = rasterio.open("nat_color.tif")
pyplot.imshow(src.read(1), cmap='pink')
pyplot.show = lambda : None
pyplot.show()