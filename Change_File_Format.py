#iterate through folder of images change file name and type and delete original

import glob
import os 
import subprocess
import gdal       
import time       
  
 #define input files
images = glob.glob(filepath)

#iteret oveer and use gdal warp to create new file
for img in images[:]:
    #define new filename with new extentions
    outimg = img[:-4]+'.NEW FORMAT'
    #call warp to make new file
    gdal.Warp( outimg, img, options = gdal.WarpOptions(format = 'NEW FORMAT', multithread = True))
    #delay to ensure file fully closed
    time.sleep(5)
    #remove original file
    os.remove(img)
    
