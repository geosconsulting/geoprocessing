import os
import numpy as np
from osgeo import gdal
import ospybook as pb


os.chdir('../dati/osgeopy-data/Massachusetts/')
in_fn = 'm_4207162_ne_19_1_20140718_20140923_clip.tif'
out_fn = 'ndvi.tif'

ds = gdal.Open(in_fn)
red = ds.GetRasterBand(1).ReadAsArray().astype(np.float)
nir = ds.GetRasterBand(4).ReadAsArray()

# Mask the red band.
red = np.ma.masked_where(nir + red == 0, red)

# ALTERNATIVA salvando la maschera e applicandola ad altri files
# mask = np.ma.equal(nir + red, 0)
# red = np.ma.masked_array(red, mask)

# Do the calculation.
ndvi = (nir - red) / (nir + red)

# Esempio Array Mascherato
# a = np.array([0, 1, 2, 3])
# b = np.ma.masked_where(a <= 2, a)
# print a,b

ndvi = ndvi.filled(-99)

out_ds = pb.make_raster(ds,out_fn,ndvi,gdal.GDT_Float32,-99)
overviews = pb.compute_overview_levels(ds.GetRasterBand(1))
out_ds.BuildOverviews('average',overviews)
del ds,out_ds

