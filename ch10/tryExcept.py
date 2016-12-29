import os
import glob
import gdal
import logging

# importante senno becco sempre l'errore
gdal.UseExceptions()

os.chdir('../dati/osgeopy-data/Switzerland/')
file_list = glob.glob('*.tif')
print file_list
print

file_list_manuale = ['dem_class.tif', 'dem_class2.tiff', 'dem_class3.tif']
for fn in file_list_manuale:
    try:
        print "Statitics for %s " % fn
        ds = gdal.Open(fn)
        print "MIN,MAX,MEAN,STD"
        print ds.GetRasterBand(1).ComputeStatistics(True)

        print "67% dati tra %0.2f and 0.2f" % ()
        # print ds.GetRasterBand(1).GetStatistics(0,1)
        print
    except:
        print('Could nor capute stats for ' + fn)
        print(gdal.GetLastErrorMsg())
        # logging.basicConfig(filename="log.txt")