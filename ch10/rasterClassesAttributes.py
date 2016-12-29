import os
import gdal

os.chdir('../dati/osgeopy-data/Switzerland/')
DS = gdal.Open('dem_class2.tif')
BAND = DS.GetRasterBand(1)
BAND.SetNoDataValue(-1)

rat = gdal.RasterAttributeTable()
rat.CreateColumn('Valore',gdal.GFT_Integer,gdal.GFU_Name)
rat.CreateColumn('Conteggio',gdal.GFT_Integer,gdal.GFU_PixelCount)
rat.CreateColumn('Elevazione',gdal.GFT_String,gdal.GFU_Generic)
rat.SetRowCount(6)

rat.WriteArray(range(6),0)
rat.WriteArray(BAND.GetHistogram(-0.5,5.5,6,False,False),1)
rat.SetValueAsString(1,2,'0-800')
rat.SetValueAsString(2,2,'800-1300')
rat.SetValueAsString(3,2,'1300-2000')
rat.SetValueAsString(4,2,'2000-2600')
rat.SetValueAsString(5,2,'2600 +')

BAND.SetDefaultRAT(rat)
BAND.SetNoDataValue(0)
del BAND,DS
