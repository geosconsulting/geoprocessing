import pandas as pd
import geopandas as gpd

fn = 'dati/osgeopy-data/global/ne_50m_populated_places.shp'
gdf = gpd.read_file(fn)

lista = [1,2,3,4,5]
lista1 = [6,7,8,9,10]
lista2 = [11,12,13,14,15]
righe = ['a','b','c']
df = pd.DataFrame([lista, lista1, lista2],index=righe,columns=('A','B','C','D','E'))
print df

dict_conv = {'A': (1, 2, 3, 4,), 'B': (5, 6, 7, 8)}
df_conv = pd.DataFrame(dict_conv)
print df_conv