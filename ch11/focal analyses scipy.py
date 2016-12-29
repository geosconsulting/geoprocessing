# Script to smooth an elevation dataset.
import os
import scipy.ndimage
from osgeo import gdal
import ospybook as pb

in_fn = "../dati/osgeopy-data/Nepal/everest.tif"
out_fn = 'everest_smoothed.tif'

in_ds = gdal.Open(in_fn)
in_data = in_ds.GetRasterBand(1).ReadAsArray()

out_data = scipy.ndimage.filters.uniform_filter(in_data, size=3, mode='nearest')

pb.make_raster(in_ds, out_fn, out_data, gdal.GDT_Int32, -99)
del in_ds
