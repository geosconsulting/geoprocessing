import os
import gdalnumeric

os.chdir('../dati/osgeopy-data/Washington/dem')
src = "tfc.tif"

arr = gdalnumeric.LoadFile(src)

gdalnumeric.SaveArray(arr[[0,1,2],:],"falco.tif",format="GTiff", prototype=src)
gdalnumeric.SaveArray(arr[[1,2,3],:],"talco.tif",format="GTiff", prototype=src)


