"""
    create shell script of all images in fodler to chagne file format using GDAL translate
    """

import glob
import os

#file path for images to chagne file format
images = glob.glob('/Users/maddie/Desktop/VideoClassifications/*.kea')

#output bas shell script to be run in terminal
outfile = ('/Users/maddie/Desktop/VideoClassifications/ShellScript.sh')
#write commands to shell script
ofile = open(outfile, 'w+')
for img in images:
    name = os.path.splitext(os.path.split(img) [-1]) [0]
    #define new file name and path for output file type
    outpath = os.path.join('/Users/maddie/Desktop/VideoClassifications/Binary/', name + ".jpeg")
    #write command to ouptu file
    ofile.write("gdal_translate -of JPEG -expand RGB "+ img+ " "+ outpath + "\n" )
#close out file
ofile.flush()
ofile.close()

