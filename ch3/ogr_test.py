from osgeo import ogr

driver = ogr.GetDriverByName('geojson')
print driver

import ospybook as pb
pb.print_drivers()
