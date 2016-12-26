import os
import urllib
from osgeo import ogr
import folium

def get_bbox(geom):
    return '{0},{1},{2},{3}'.format(*geom.GetEnvelope())

def get_center(geom):
    centroid = geom.Centroid()
    return [centroid.GetY(),centroid.GetX()]

def get_state_geom(state_name):
    # C:\Users\Fabio\Documents\Programmazione\PycharmProjects\geoprocessing\dati\osgeopy - data\US\states.geojson
    ds = ogr.Open('c:/Users/Fabio/Documents/Programmazione/PycharmProjects/geoprocessing/dati/osgeopy-data/US/states.geojson')

    if ds is None:
        raise RuntimeError(
            'Could not open the states dataset. Is the path correct?'
        )
    lyr = ds.GetLayer()
    lyr.SetAttributeFilter('state = "{0}"'.format(state_name))
    feat = next(lyr)
    return feat.geometry().Clone()

def save_state_gauges(out_fn,bbox=None):
    url = 'http://gis.srh.noaa.gov/arcgis/services/ahps_gauges/' + \
          'MapServer/WFSServer'
    parms = {
        'version': '1.1.0',
        'typeNames': 'ahps_gauges:Observed_River_Stages',
        'srsName': 'urn:ogc:def:crs:EPSG:6.9:4326',
    }
    if bbox:
        parms['bbox']= bbox
    try:
        request = 'WFS:{0}?{1}'.format(url, urllib.urlencode(parms))
    except:
        request = 'WFS:{0}?{1}'.format(url, urllib.parse.urlencode(parms))

    wfs_ds = ogr.Open(request)
    if wfs_ds is None:
        raise RuntimeError('Could not open WFS')
    wfs_lyr = wfs_ds.GetLayer(0)

    driver = ogr.GetDriverByName('GeoJSON')
    if os.path.exists(out_fn):
        driver.DeleteDataSource(out_fn)
    json_ds = driver.CreateDataSource(out_fn)
    json_ds.CopyLayer(wfs_lyr,'')

    feat = wfs_lyr.GetNextFeature()

def make_map(state_name,json_fn,html_fn,**kwargs):
    geom = get_state_geom(state_name)
    save_state_gauges(json_fn,get_bbox(geom))
    fmap = folium.Map(location=get_center(geom),**kwargs)
    fmap.geo_json(geo_path=json_fn)
    fmap.create_map(path=html_fn)

# os.chdir(r'C:\Users\Fabio\Dropbox\webmaps')
make_map('Oklahoma','ok.json','ok.html',zoom_start=7)