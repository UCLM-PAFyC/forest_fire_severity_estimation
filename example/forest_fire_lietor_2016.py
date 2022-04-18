import ee 
from ee_plugin import Map 
from ee import batch

def addNBR(image):
    """A function to compute NDVI."""
    ndvi = image.normalizedDifference(['B8', 'B12']).rename('nbr')
    return image.addBands([ndvi])

# Definicion del area de interes: sw,nw,ne,se
roi = ee.Geometry.Polygon([
    [[-1.90, 38.51],[-1.90, 38.55], [-1.83, 38.55], [-1.83, 38.51]]
])

prefire_start = '2016-06-01';   
prefire_end = '2016-06-29';

postfire_start = '2016-07-06';
postfire_end = '2016-08-05';

prefire_collection = ee.ImageCollection('COPERNICUS/S2')\
    .filterDate(prefire_start, prefire_end)\
    .filterMetadata ('CLOUDY_PIXEL_PERCENTAGE', 'Less_Than', 10)\
    .map(addNBR)\
    .filterBounds(roi)\
    .max()
prefire_nbr = prefire_collection.select('nbr')

postfire_collection = ee.ImageCollection('COPERNICUS/S2')\
    .filterDate(postfire_start, postfire_end)\
    .filterMetadata ('CLOUDY_PIXEL_PERCENTAGE', 'Less_Than', 10)\
    .map(addNBR)\
    .filterBounds(roi)\
    .min()
postfire_nbr = postfire_collection.select('nbr')

dNBR_unscaled = prefire_nbr.subtract(postfire_nbr)
dNBR = dNBR_unscaled.multiply(1000)
Map.addLayer(dNBR,  {'min': -1000, 'max': 1000}, 'dNBR S2')

severity_file_name = 'ForestFireLietor2006SeverityDNBR'

task = ee.batch.Export.image.toDrive(image=dNBR,
region=roi,
folder='gee_results',
scale=10,
# fileFormat: 'GeoTIFF', 
fileNamePrefix=severity_file_name,
crs='EPSG:25830')
task.start()

print('Ended process ')


