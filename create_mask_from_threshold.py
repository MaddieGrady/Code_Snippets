# !/usr/bin env python 

import gdal 
import numpy as np 

image_file = r"PATH TO IMAGE FILE"
out_mask_file = r"PATH TO MASK FILE OUTPUT"


#open the image dataset
ds = gdal.Open(image_file)
#open data from band 1 as numpy array 
df = ds.GetRasterBand(1).ReadAsArray()

#create new numpy array of same size as image array 
mask_array = np.zeros_like(df)

#populate mask array based on threshold
#set threshold value
threshold = 100
#make values greater than threshold in array have value 1
#if not greater than 1 value will remain 0
mask_array = np.where((df > threshold), 1, mask_array)
#make values less than threshold 2 but leave no data (assume 0) as 0 in mask
mask_array = np.where(((df < threshold) & (df != 0)), 2, mask_array)

#write mask array to output file
#output to file
#define file type driver (geotiff)
driver = gdal.GetDriverByName("GTiff")
#create dataset of same size as open image , 1 band and data type interger
dst_dataset = driver.Create(out_mask_file, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Int16)
#set projection info to be the same as input image file
dst_dataset.SetGeoTransform(ds.GetGeoTransform())
dst_dataset.SetProjection(ds.GetProjection())
#write mask array to data in band 1
dst_dataset.GetRasterBand(1).WriteArray(mask_array)
dst_dataset = None 

