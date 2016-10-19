import sys
from osgeo import ogr
import os

fn = '../dati/osgeopy-data/global/ne_50m_populated_places.shp'
ds = ogr.Open(fn, 0)
if ds is None:
    sys.exit(('Could not open {0}.'.format(fn)))
lyr = ds.GetLayer(0)

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
for field in lyr.schema:
    print field.name, field.GetTypeName()

i = 0
for feat in lyr:
    pt = feat.geometry()
    x = pt.GetX()
    y = pt.GetY()
    name = feat.GetField('NAME')
    pop = feat.GetField('POP_MAX')
#    print(name, pop, x, y)
    i += 1
    if i == 10:
        break

del ds


# from ospybook.vectorplotter import VectorPlotter
# vp = VectorPlotter(True)
# vp.plot(fn, 'bo')
# vp.show('test')


