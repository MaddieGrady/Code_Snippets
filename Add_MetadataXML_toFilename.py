"""
    Extract information from metadata provided in XML documents and add to filename
    XML and image data to change filename should be in the same folder
    assumes the xml and image data have the same file name for each image
"""
#import required modules, all are provided in core python
import glob
import os
import xml.etree.ElementTree as ET


#search for images
tif_files = sorted(glob.glob("search_path"+"/*.tif"))
xml_files = sorted(glob.glob("search_path"+"/*.xml"))

#define the folder for changed image files to go in could be the same as input folder
out_folder = "output file path"

#loop through images and identify data in metadata and rename files
for tif, xml in zip(tif_files, xml_files):
#define xml namespace if one provided
    ns = {'ns':"http:www.examplenamespace.com"}
    #open the xml file
    tree = ET.parse(xml)
    root = tree.getroot()

    #extract the data required from xml
    data = root.find('ns:datalabel', ns).text

    out_tif = os.path.join(out_folder, "output file name"+data+".tif")

    os.rename(tif, out_tif)




