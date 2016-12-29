# Script to smooth an elevation dataset.
import os
import sys
from osgeo import gdal,ogr

folder = r"C:\Users\Fabio\Documents\Programmazione\PycharmProjects\geoprocessing\dati\osgeopy-data\Idaho"
print(os.path.isdir(folder))

roads_ln = 'allroads'
print(os.path.exists(folder+'/'+roads_ln+'.shp'))

wilderness_ln = 'wilderness'
road_raster_fn = 'church_roads.tif'
proximity_fn = 'proximity.tif'
cellsize = 10

shp_ds = ogr.Open(folder)
wild_lyr = shp_ds.GetLayerByName(wilderness_ln)
wild_lyr.SetAttributeFilter("WILD_NM = 'Frank Church - RONR'")
envelopes = [row.geometry().GetEnvelope() for row in wild_lyr]
coords = list(zip(*envelopes))

minx,maxx = min(coords[0]),max(coords[1])
miny,maxy = min(coords[2]),max(coords[3])

road_lyr = shp_ds.GetLayerByName(roads_ln)
road_lyr.SetSpatialFilterRect(minx,miny,maxx,maxy)

os.chdir(folder)
tif_driver = gdal.GetDriverByName('GTiff')
cols = int((maxx-minx)/cellsize)
rows = int((maxy-miny)/cellsize)

road_ds = tif_driver.Create(road_raster_fn,cols,rows)
road_ds.SetProjection(road_lyr.GetSpatialRef().ExportToWkt())
road_ds.SetGeoTransform((minx,cellsize,0,maxy,0,-cellsize))

gdal.RasterizeLayer(road_ds,[1],road_lyr,burn_values=[1], callback = gdal.TermProgress)

prox_ds = tif_driver.Create(proximity_fn,cols,rows,1,gdal.GDT_Int32)
prox_ds.SetProjection(road_ds.GetProjection())
prox_ds.SetGeoTransform(road_ds.GetGeoTransform())
gdal.ComputeProximity(road_ds.GetRasterBand(1),prox_ds.GetRasterBand(1),['DISTUNITS=GEO'], gdal.TermProgress)

wild_ds = gdal.GetDriverByName('MEM').Create('tmp',cols,rows)
wild_ds.SetProjection(prox_ds.GetProjection())
wild_ds.SetGeoTransform(prox_ds.GetGeoTransform())
gdal.RasterizeLayer(wild_ds,[1],wild_lyr,burn_values=[1], callback=gdal.TermProgress)

wild_data = wild_ds.ReadAsArray()
prox_data = prox_ds.ReadAsArray()

prox_data[wild_data == 0] = -99
prox_ds.GetRasterBand(1).WriteArray(prox_data)
prox_ds.GetRasterBand(1).SetNoDataValue(-99)
prox_ds.FlushCache()

stats = prox_ds.GetRasterBand(1).ComputeStatistics(False,gdal.TermProgress)
print('Mean distance from road is',stats[2])

del prox_ds,road_ds,shp_ds

