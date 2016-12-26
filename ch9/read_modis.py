import os
import gdal

os.chdir('../dati/osgeopy-data/Modis/')
src = "MYD13Q1.A2014313.h20v11.005.2014330092746.hdf"

ds = gdal.Open(src)
subdatasets = ds.GetSubDatasets()
print('Number of subdatasets: {}'.format(len(subdatasets)))

for sd in subdatasets:
 print('Name: {0}\nDescription:{1}\n'.format(*sd))

 ndvi_ds = gdal.Open(subdatasets[0][0])

# subdatasets[4][0] to open the fifth subdataset
ndvi_ds = gdal.Open(subdatasets[4][0])
