#import required modules
import os
import glob
import rsgislib
import shutil
from rsgislib import vectorutils
from rsgislib import imagecalc
import argparse

"""
    RASTERISE FOLDER OR INDIVIDUAL SHAPEFILE USING RSGISLIB FROM COMMAND LINE
    
    REQUIRES RASTER IMAGE TO RASTERISE TO IF CAN SUPPLY DIFFERNENT RASTERS BUT INPUTS
    MUST BE OF SAME LENGTH AS VECTORS
    
    """
def Rasterise(InputPath, InputFile, OutputPath, NewOutputName, InputRaster, InputRasterPath):
    tmpPath = './tmp/'
    if not os.path.isdir(tmpPath):
        os.makedirs(tmpPath)
    
    if not os.path.isdir(OutputPath):
        os.makedirs(OutputPath)
    
    Images = sorted(glob.glob(InputPath+"/*.shp")) if InputPath!=None else InputFile
    Raster = sorted(glob.glob(InputRasterPath+"/*.kea")) if InputRasterPath!=None else InputRaster

    print(len(Images))
    print(len(Raster))

    if len(Images) == len(Raster):
        for InVec, InImg in zip(Images, Raster):
            print("Processing :" + InVec)
            BaseName = os.path.splitext(os.path.split(InVec) [-1]) [0]
            FinalImg = os.path.join(OutputPath, BaseName + ".kea") if NewOutputName == None else os.path.join(OutputPath, NewOutputName + ".kea")
            outImage = os.path.join(tmpPath, BaseName + ".kea")
            vectorutils.rasterise2Image(InVec, InImg, outImage, 'KEA', burnVal=1, shpAtt=None, shpExt=False)
            imagecalc.allBandsEqualTo(outImage, 0, 0, 1, FinalImg, 'KEA', rsgislib.TYPE_16INT)
            print("Finished:" + InVec)

    elif len(Raster) == 1:
        for Img in Images:
            print("Processing :" + InVec)
            BaseName = os.path.splitext(os.path.split(Img) [-1]) [0]
            FinalImg = os.path.join(OutputPath, BaseName + ".kea") if NewOutputName == None else os.path.join(OutputPath, NewOutputName + ".kea")
            outImage = os.path.join(tmpPath, BaseName + ".kea")
            vectorutils.rasterise2Image(Img, Raster, outImage, 'KEA', burnVal=1, shpAtt=None, shpExt=False)
            imagecalc.allBandsEqualTo(outImage, 0, 0, 1, FinalImg, 'KEA', rsgislib.TYPE_16INT)
            print("Finished:" + InVec)

    else:
        raise("More than 1 Raster Defined but number does not match number of input vectors")
        shutil.rmtree(tmpPath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'RasteriseShapefiles.py', description = '''Rasterise Shapefiles/Create Mask Image from Shapefiles''')
    parser.add_argument("-i", "--InputPath", help = '''Path to Input Files (Shapefile .shp)''', required = False, default = None)
    parser.add_argument("-f", "--InputFile", help = '''Path to Individual Input File''', required = False, default =None)
    parser.add_argument("-o", "--OutputPath", help = '''Path to Output File Locations''', required = True, default = None)
    parser.add_argument("-n", "--NewOutputName", help = '''New Output File Name, if None will use input Name''', required = False, default = None)
    parser.add_argument("-r", "--RasterImage", help = '''Image extent and projection to rasterise the vector data to''', required = False, default = None)
    parser.add_argument("-t", "--RasterImages", help='''Extent and projection to reasterise the vector data to if multiple images are needed, Input Path to folder of raster images Raster (.kea)''', required = False, default = None)
    
    args = parser.parse_args()

Rasterise(args.InputPath, args.InputFile, args.OutputPath, args.NewOutputName, args.RasterImage, args.RasterImages)
