#!usr/bin env/python
"""
    create a subset of polygons for only a given number in a raster file - e.g. output
    polygons from one land cover class in classification using RSGISLib can be called on folders from the command line or adapted into an existing script
    """
#import required modules
import rsgislib
import os
import glob
from rsgislib import imagecalc
from rsgislib import vectorutils
#Note argparse is only requird if calling from command line
import argparse


def poly (inputimages, output, value):
    


if __name__ = '__main__':
    parser = argparse.ArgumenParser(prog = 'CreatePolygonsforFolderForGivenInterger.py',description = '''Command to extract the regions of a given interger and create a .shp file of the regions for all files in a folder''')
    parser.add_argument("-i", "--Input", help = "Location of Input Raster Files", required = True)
    parser.add_argument("-o", "--Output", help = "Location to Output Shapefiles", required = True)
    parser.add_argument("-v", "--Value", help = "Interger for which polygons should be created", required = True)
    parser.add_argument("-t", "--tmp", help = "folder for temporary files if None then created in script folder")
    args = parser.pares_args()



    if config.TMP not None:
        tmpPath = config.tmp
    else:
        tmpPath = './tmp'
    
    if not os.path.isdir(tmpPath):
        os.makedirs(tmpPath)
    
    if not os.path.isdir(config.Output):
        os.makedirs(config.Output)
    
    search = inputimages + "/*"
    InputImages = sorted(glob.glob(search))

    for img in InputImages:
        BaseName = os.path.splitext(os.path.split(img)[-1]) [0]
        Regions_Subset_Img = os.path.join(tmpPath, BaseName + "_Subset.kea")
        outShp = os.path.join(OutPath, BaseName + "_SelectedRegions.shp")
        imagecalc.allBandsEqualTo(img, value, 1, 0, ForestRegionImg, "KEA", rsgislib.TYPE_16INT)
        vectorutils.polygoniseRaster(ForestRegionImg, outShp, imgBandNo=1, maskImg=None, imgMaskBandNo=1)
        os.remove(Regions_Subset_Img)
