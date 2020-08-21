
#!usr/bin env/python

import os.path
# Import the python sys module
import sys
# Import the python glob module
import glob
#  import the fnmatch module
import fnmatch
# Import the python Argument parser
import argparse
# Import os.walk to navigate directory structure.
import os
# Import ogr
import ogr

"""
    BUFFER SHAPEFILES BY GIVEN MAP UNIT.
    
    CONFIG PARSER OPTIONS AT END OF SCRIPT
    
    CALL FROM COMMAND LINE
    """

def buffer(InputPath, InputFile, OutputFile, OutputPath, NewOutputName, Buffer):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    BufferDistance = int(Buffer)
    if InputFile != None and OutputFile != None:
        print("Buffering Single Image File")
        FileDataset = ogr.Open(InputFile)
        if FileDataset == None:
            raise Exception ("Could Not Open Input File")
        if os.path.exists(OutputFile):
            driver.DeleteDataSource(OutputFile)
        FileLayer = FileDataset.GetLayer()
        OutputBuffer = driver.CreateDataSource(OutputFile)
        bufferlyr = OutputBuffer.CreateLayer(OutputFile, geom_type=ogr.wkbPolygon)
        featureDefn = bufferlyr.GetLayerDefn()
        
        for feature in FileLayer:
            ingeom = feature.GetGeometryRef()
            buffergeom = ingeom.Buffer(BufferDistance)
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(buffergeom)
            bufferlyr.CreateFeature(outFeature)
            outFeature = None


if InputFile != None and OutputFile == None:
    print("Buffering Single Image File")
    FileDataset = ogr.Open(InputFile)
    if FileDataset == None:
        raise Exception ("Could Not Open Input File")
        if NewOutputName == None:
            BaseName = os.path.splitext(os.path.split(inFile) [-1]) [0]
            outfile = os.path.join(OutputPath, BaseName + "_Buffer_" + Buffer+".shp")
    elif NewOutputName != None:
        outfile = os.path.join(OutputPath, NewOutputName+ "_Buffer_" + Buffer+".shp")
        if os.path.exists(OutputFile):
            driver.DeleteDataSource(OutputFile)
FileLayer = FileDataset.GetLayer()
OutputBuffer = driver.CreateDataSource(OutputFile)
bufferlyr = OutputBuffer.CreateLayer(outfile, geom_type=ogr.wkbPolygon)
featureDefn = bufferlyr.GetLayerDefn()

for feature in FileLayer:
    ingeom = feature.GetGeometryRef()
    buffergeom = ingeom.Buffer(BufferDistance)
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(buffergeom)
    bufferlyr.CreateFeature(outFeature)
    outFeature = None
    
    if InputPath != None and OutputPath != None:
        print("Buffering Multiple Image Files")
        print(InputPath)
        Search = InputPath + "/*.shp"
        InputFilesList = sorted(glob.glob(Search))
        print(InputFilesList)
        if len(InputFilesList) == 0:
            raise Exception("Could Not Locate Shapefiles")
        for inFile in InputFilesList:
            print("Buffering: " + inFile)
            FileDataset = ogr.Open(inFile)
            if FileDataset == None:
                raise Exception ("Could Not Open Input File")
            if NewOutputName == None:
                BaseName = os.path.splitext(os.path.split(inFile) [-1]) [0]
                outfile = os.path.join(OutputPath, BaseName + "_Buffer_" + Buffer+".shp")
            elif NewOutputName != None:
                outfile = os.path.join(OutputPath, BaseName+ "_Buffer_" + Buffer+".shp")
            if os.path.exists(outfile):
                driver.DeleteDataSource(outfile)
            FileLayer = FileDataset.GetLayer()
            OutputBuffer = driver.CreateDataSource(outfile)
            bufferlyr = OutputBuffer.CreateLayer(outfile, geom_type=ogr.wkbPolygon)
            featureDefn = bufferlyr.GetLayerDefn()
            
            for feature in FileLayer:
                ingeom = feature.GetGeometryRef()
                buffergeom = ingeom.Buffer(BufferDistance)
                outFeature = ogr.Feature(featureDefn)
                outFeature.SetGeometry(buffergeom)
                bufferlyr.CreateFeature(outFeature)
                outFeature = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'BufferShapefile.py', description = '''Command to Buffer Existing Shapefile Regions''')
    parser.add_argument("-i", "--InputPath", help = '''Path to Input Files no spaces ("File Location *.shp" )''', required = False, default = None)
    parser.add_argument("-f", "--InputFile", help = '''Path to Individual Input File''', required = False, default =None)
    parser.add_argument("-o", "--OutputFile", help = '''Path to Individual Output File''', required = False, default = None)
    parser.add_argument("-p", "--OutputPath", help = '''Path to Output File Locations''', required = False, default = None)
    parser.add_argument("-n", "--NewOutputName", help = '''New Output File Name, if None will use input Name''', required = False, default = None)
    parser.add_argument("-b", "--BufferDistance", help = '''Buffer Distance uses map units''', required = True)
    
    args = parser.parse_args()
    
    inputIsDIR = True

buffer(args.InputPath, args.InputFile, args.OutputFile, args.OutputPath, args.NewOutputName, args.BufferDistance)
