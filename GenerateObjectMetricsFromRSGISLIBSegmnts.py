"""
    convert rsgislib segmentation output to vector and calculate metrics from shapes
    add metrics back to RAT in KEA clumps file
    """
#import required modules

import glob, rsgislib, os, ogr, gdal, osr, math
import numpy as np
import rios
from rios import rat
from rios import ratapplier
from rsgislib.segmentation import segutils

#import iamges and run segmentation see rsgislib for parameters
image = 'file path for image to segment'

clumps = 'file path for segmentation image'

segutils.runSheppardSegmentation(image,
                                 clumps,
                                 tmppath = 'file path for tmp images')

out_shp = 'file path for polygons of segments'
veclyr = os.path.split(out_shp)[-1].split('.')[0]
#genrate polygons of segments
#note if there are no data regions e.g. edges of a mosaic a valid data mask will also be
#needed see rsgislib
vectorutils.polygoniseRaster(clumps, out_shp)

#calcuate metrics from shapes
#open the Shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
dataSource = driver.Open(out_shp, 1)
layer = dataSource.GetLayer()
#generate the new fields in the attribute table
new_field_area = ogr.FieldDefn("Area", ogr.OFTReal)
new_field_area.SetWidth(32)
new_field_area.SetPrecision(3)
layer.CreateField(new_field_area)
new_field_Length = ogr.FieldDefn("Length", ogr.OFTReal)
new_field_Length.SetWidth(32)
new_field_Length.SetPrecision(3)
layer.CreateField(new_field_Length)
new_field_BB_Elongation = ogr.FieldDefn("BB_Elongat", ogr.OFTReal)
new_field_BB_Elongation.SetWidth(32)
new_field_BB_Elongation.SetPrecision(3)
layer.CreateField(new_field_BB_Elongation)
new_field_Length = ogr.FieldDefn("BB_Area", ogr.OFTReal)
new_field_BB_Area.SetWidth(32)
new_field_BB_Area.SetPrecision(3)
layer.CreateField(new_field_BB_Area)
new_field_Thinness_R = ogr.FieldDefn("Thinness_R", ogr.OFTReal)
new_field_Thinness_R.SetWidth(32)
new_field_Thinness_R.SetPrecision(3)
layer.CreateField(new_field_Thinness_R)
#calcualte statiscs for each object
for feature in layer:
    area = feature.GetGeometryRef().GetArea()
    feature.SetField("Area", area)
    length = feature.GetGeometryRef().Boundary().Length()
    feature.SetField("Length", length)
    #calculate elongation of bounding box
    envelope = feature.GetGeometryRef().GetEnvelope()
    xlength = envelope[1] - envelope[0]
    ylength = envelope[3] - envelope[2]
    diff = min([xlength, ylength])/max([xlength, ylength])
    #calcualte thinness ratio
    area = xlength*ylength
    l2 = length*length
    pival = math.pi
    thinnes = 4 * pival * (area/ l2)

    feature.SetField("BB_Elongat", diff)
    feateur.SetField("BB_Area", area)
    feature.SetField("Thinnes_R", thinness)
    layer.SetFeature(feature)

#close data set
dataSource = None

# add to RAT of segmentaiton file
rastergis.importVecAtts(clumps, out_shp, veclyr, 'PXLVAL', ['Area', 'Length', 'BB_Elongat', ' BB_Area', 'Thinnes_R'] )


