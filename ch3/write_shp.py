import sys
from osgeo import ogr

#Open directory not file
fd = '../dati/osgeopy-data/global'
ds = ogr.Open(fd, 1)
if ds is None:
    sys.exit(('Could not open folder {0}.'.format(fd)))
lyr = ds.GetLayer(0)
print "LAYER NAME Index 0 {0}".format(lyr.GetName())

in_lyr = ds.GetLayer('ne_50m_populated_places')

num_features = lyr.GetFeatureCount()
print "Numero features {0}".format(num_features)
last_feature = lyr.GetFeature(num_features-1)
# print last_feature.NAME

print "Estensione features {0}".format(lyr.GetExtent())
print "Tipo geometria features {0}".format(lyr.GetGeomType())
feat = lyr.GetFeature(0)
print "Tipo geometria feature zero {0}".format(feat.geometry().GetGeometryName())
print "Spatial Reference {0}".format(lyr.GetSpatialRef())

#Name and type of field
print
print "-----------------------------------"
print "Campi shapefile"
print "-----------------------------------"
for field in lyr.schema:
    print field.name, field.GetTypeName()

del ds


# from ospybook.vectorplotter import VectorPlotter
# vp = VectorPlotter(True)
# vp.plot(fn, 'bo')
# vp.show('test')


