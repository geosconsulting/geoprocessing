import os
from osgeo import gdal

os.chdir(r'C:\Users\Fabio\Downloads\Studio\landsat\LC81910312016217LGN00')
band1_fn = 'intorno_casa_B2.tif'
band2_fn = 'intorno_casa_B3.tif'
band3_fn = 'intorno_casa_B4.tif'
band4_fn = 'intorno_casa_B5.tif'

in_ds = gdal.Open(band2_fn)
in_band = in_ds.GetRasterBand(1)

gtiff_driver =gdal.GetDriverByName('GTiff')
out_ds = gtiff_driver.Create('fal_color.tif', in_band.XSize, in_band.YSize, 3, in_band.DataType)
out_ds.SetProjection(in_ds.GetProjection())
out_ds.SetGeoTransform(in_ds.GetGeoTransform())

in_data = in_band.ReadAsArray()
out_band = out_ds.GetRasterBand(3)
out_band.WriteArray(in_data)

in_ds = gdal.Open(band3_fn)
out_band = out_ds.GetRasterBand(2)
out_band.WriteArray(in_ds.ReadAsArray())

out_ds.GetRasterBand(1).WriteArray(gdal.Open(band4_fn).ReadAsArray())

out_ds.FlushCache()
for i in range(1,4):
    out_ds.GetRasterBand(i).ComputeStatistics(False)

out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])
del out_ds
