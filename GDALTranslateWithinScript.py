"""
    calling gdal translate on folder of images within a python script
    """
#import required modules
import glob
import gdal
import os

filenames = sorted(glob.glob('/Users/maddie/Desktop/VideoClassifications/Change/*.kea'))#Folder of images to be translated to another file format

for filename in filenames:
    file = gdal.Open(filename)
    format = "PNG" #Format to translate to see GDAL information for list of possible
    driver = gdal.GetDriverByName(format)
    BaseName = os.path.splitext(os.path.split(filename) [-1]) [0]
    OutPath = '/Users/maddie/Desktop/VideoClassifications/Change/Video/'
    OutFilename = os.path.join(OutPath, BaseName + ".png")#Change extention to match defined format
    OutputDataset = driver.CreateCopy(OutFilename, file, 0)
    OutputDataset = None
    file = None


