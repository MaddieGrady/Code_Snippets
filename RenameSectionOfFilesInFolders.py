"""
    walk through all folders and subfolders to rename files in place files
    e.g. replaces Sen2A with Sen2
    now less usefull as glob can be used to search recursively
    """
#import required modules

import os
import shutil


#CHANGE FILE NAMES IN FOLDER
#identify the file paths for all items in folders and subfodlders
paths = (os.path.join(root, filename)
         # input file directory
         for root, _, filenames in os.walk('/Users/maddie/Desktop/VideoClassifications/Binary/')
         for filename in filenames)

#iterate through them and replace part of the file name with a new value
for path in paths:
    # the 'Sen2A' in the example below will be replaced by the 'Sen2' in the filenames in the directory
    newname = path.replace('Sen2A' , 'Sen2')
    if newname != path:
        os.rename(path, newname)

