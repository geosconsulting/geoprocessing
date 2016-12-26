import os
import numpy as np
from osgeo import gdal

os.chdir('../dati/osgeopy-data/Washington/dem')
in_ds = gdal.Open("gt30w140n90.tif")
in_band = in_ds.GetRasterBand(1)
xsize = in_band.XSize
ysize = in_band.YSize
block_xsize, block_ysize = in_band.GetBlockSize()
nodata = in_band.GetNoDataValue()

out_ds = in_ds.GetDriver().Create('dem_feet.tif', in_band.XSize, in_band.YSize, 3, in_band.DataType)
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())
out_band = out_ds.GetRasterBand(1)

for x in range(0,xsize,block_xsize):
    if x + block_xsize < xsize:
        cols = block_xsize
    else:
        cols = xsize - x
    for y in range(0, ysize, block_ysize):
        if y + block_ysize < ysize:
            rows = block_ysize
        else:
            rows = ysize - y
        data = in_band.ReadAsArray(x, y, cols, rows)
        data = np.where(data == nodata, nodata, data*3.28084)
        out_band.WriteArray(data, x, y)

out_band.FlushCache()
out_band.SetNoDataValue(nodata)
out_band.ComputeStatistics(False)

out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])
del out_ds
