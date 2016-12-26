import sys
from osgeo import ogr

# Open directory not file
fd = '../dati/osgeopy-data/global'
ds = ogr.Open(fd, 1)
# Esiste la directory che voglio aprire?
if ds is None:
    sys.exit(('Could not open folder {0}.'.format(fd)))
in_lyr = ds.GetLayer('ne_50m_populated_places')

# Esiste il file che voglio creare se si cancellalo?
if ds.GetLayer('capital_cities'):
   ds.DeleteLayer('capital_cities')

# Con Exceptions posso eveitare la
# cancellazione automatica e semplicemnete uscire dal codice
ogr.UseExceptions()
# Creo un layer vuoto con le carateristiche
# spaziali dell'esistente da cui estraggo features
try:
    out_lyr = ds.CreateLayer('capital_cities',
                   in_lyr.GetSpatialRef(),
                   ogr.wkbPoint)
    # Creo i campi presi dallo schema dell layer di ingresso
    out_lyr.CreateFields(in_lyr.schema)
    out_defn = out_lyr.GetLayerDefn()
    out_feat = ogr.Feature(out_defn)
except RuntimeError as e:
    print e
    import sys
    sys.exit()

for in_feat in in_lyr:
    if in_feat.GetField('FEATURECLA') == 'Admin-0 capital':
        # Copio la geometria dalla feature che voglio usare
        geom = in_feat.geometry()
        # La passo lla feature da inserire nel nuovo layer
        out_feat.SetGeometry(geom)
        # Copio geometria e attributi
        for i in range(in_feat.GetFieldCount()):
            value = in_feat.GetField(i)
            out_feat.SetField(i, value)
        out_lyr.CreateFeature(out_feat)

coord_fld = ogr.FieldDefn('X',ogr.OFTReal)
coord_fld.SetWidth(8)
coord_fld.SetPrecision(3)
out_lyr.CreateField(coord_fld)
coord_fld.SetName('Y')
out_lyr.CreateField(coord_fld)
coord_fld.SetName('Z')
out_lyr.CreateField(coord_fld)

for field in out_lyr.schema:
    print field.name, field.GetTypeName()
del ds

i = out_lyr.GetLayerDefn().GetFieldIndex('Z')


