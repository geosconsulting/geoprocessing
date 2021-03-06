import os
from osgeo import gdal
import numpy as np

os.chdir(r'C:\Users\Fabio\Downloads\Studio\landsat\LC81910312016217LGN00')

bnd_coastal_aerosol = 'LC81910312016217LGN00_B1.TIF'
bnd_blu = 'LC81910312016217LGN00_B2.TIF'
bnd_verde = 'LC81910312016217LGN00_B3.TIF'
bnd_rossa = 'LC81910312016217LGN00_B4.TIF'
bnd_nir = 'LC81910312016217LGN00_B5.TIF'
bnd_swir1 = 'LC81910312016217LGN00_B6.TIF'
bnd_swir2 = 'LC81910312016217LGN00_B7.TIF'
bnd_pan =   'LC81910312016217LGN00_B8.TIF'
bnd_cirrus = 'LC81910312016217LGN00_B9.TIF'
# TIR Thermal Infrared Sensor
bnd_tir1 = 'LC81910312016217LGN00_B10.TIF'
bnd_tir2 = 'LC81910312016217LGN00_B11.TIF'

bande_utili = (bnd_coastal_aerosol,bnd_blu, bnd_verde, bnd_rossa, bnd_nir, bnd_swir1, bnd_swir2)

in_ds_test = gdal.Open(bnd_blu)
in_band_test = in_ds_test.GetRasterBand(1)

origine_taglio_x,origine_taglio_y = 4000,3500
offset_taglio_x,offset_taglio_y = 1000, 1000

contatore = 1
for bnd in bande_utili:
    print "Banda %d" % contatore
    in_ds = gdal.Open(bnd)
    num_pixels_x_file = int(in_ds.RasterXSize)
    num_pixels_y_file = int(in_ds.RasterYSize)
    print("Pixels X %d Pixels Y %d" % (num_pixels_x_file, num_pixels_y_file))

    in_band = in_ds.GetRasterBand(1)
    # nodata = in_band.GetNoDataValue()
    num_pixels_x_bnd = int(in_band.XSize)
    num_pixels_y_bnd = int(in_band.YSize)
    # print("Pixels X %d Pixels Y %d" % (num_pixels_x_bnd, num_pixels_y_bnd))

    # ATTENZIONE GetGeoTransform dal file aperto con Open non da GetRasterBand
    parametri_geotransform = in_ds.GetGeoTransform()
    origine_x = int(parametri_geotransform[0])
    origine_y = int(parametri_geotransform[3])
    print("Origine X %d Origine Y %d" % (origine_x, origine_y))
    print ("Pixelsize X %d Pixelsize Y %d" % (parametri_geotransform[1], parametri_geotransform[5]))

    geotransform_inversa = gdal.InvGeoTransform(parametri_geotransform)
    # Converte coordinate in pixel
    conversion_pixel = gdal.ApplyGeoTransform(geotransform_inversa, 250000, 4500000)

    # Converte pixel in coordinate
    conversion_coords = gdal.ApplyGeoTransform(parametri_geotransform, origine_taglio_x, origine_taglio_y)
    xoff, yoff = map(int, conversion_pixel)
    geo_transform = (conversion_coords[0], parametri_geotransform[1], 0, conversion_coords[1], 0,
                     parametri_geotransform[5])  # complete random/arbitrary numbers

    in_data = in_band.ReadAsArray(origine_taglio_x, origine_taglio_y, offset_taglio_x, offset_taglio_y).astype(float)
    postfisso = bnd.split("_")[1].split(".")[0]
    out_ds = in_ds.GetDriver().Create('intorno_casa_' + postfisso +'.tif', in_data.shape[0], in_data.shape[0], 1, in_band.DataType)
    out_ds.SetGeoTransform(geo_transform)
    out_ds.SetProjection(in_ds.GetProjection())
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(in_data)
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    out_ds.BuildOverviews('average', [2, 4, 8, 16, 32])
    contatore += 1
del out_ds


bnd_coastal_aerosol_cut = 'intorno_casa_B1.TIF'
bnd_blu_cut = 'intorno_casa_B2.TIF'
bnd_verde_cut = 'intorno_casa_B3.TIF'
bnd_rossa_cut = 'intorno_casa_B4.TIF'
bnd_nir_cut = 'intorno_casa_B5.TIF'
bnd_swir1_cut = 'intorno_casa_B6.TIF'
bnd_swir2_cut = 'intorno_casa_B7.TIF'

bande_utili_cut = (bnd_coastal_aerosol_cut,bnd_blu_cut, bnd_verde_cut, bnd_rossa_cut, bnd_nir_cut,
               bnd_swir1_cut, bnd_swir2_cut)

in_ds_test_cut = gdal.Open(bnd_blu_cut)
in_band_test_cut = in_ds_test_cut.GetRasterBand(1)

def banda_1_7(file_bande,file_nome,ds_test,band_test):

    out_ds_landsat = in_ds.GetDriver().Create(file_nome + '.tif', band_test.XSize, band_test.YSize,
                                              len(bande_utili), band_test.DataType)
    out_ds_landsat.SetProjection(ds_test.GetProjection())
    out_ds_landsat.SetGeoTransform(ds_test.GetGeoTransform())

    for banda_attiva in file_bande:

        print "Copio banda %s" % banda_attiva
        # totale
        # indice_nuova_banda = int(banda_attiva.split('_')[1].split('.')[0].split('B')[1])
        # cut
        indice_nuova_banda=int(banda_attiva.split('_')[2].split('.')[0].split('B')[1])
        in_ds_all = gdal.Open(banda_attiva)
        in_band_all = in_ds_all.GetRasterBand(1)
        data = in_band_all.ReadAsArray()
        out_band_all = out_ds_landsat.GetRasterBand(indice_nuova_banda)
        out_band_all.WriteArray(data)
        out_band_all.FlushCache()
        # out_band.SetNoDataValue(nodata)
        out_band_all.ComputeStatistics(False)


    out_ds_landsat.BuildOverviews('average', [2, 4, 8, 16, 32])
    del out_ds_landsat

banda_1_7(bande_utili_cut,'intorno_casa',in_ds_test_cut,in_band_test_cut)