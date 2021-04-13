# !/usr/bin env python 

import gdal 
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats


image_file_1 = r"PATH TO IMAGE FILE"
mask_file = r"PATH TO MASK FILE"
image_file_2 = r"PATH TO IAMGE FILE"

#open the image dataset
ds1 = gdal.Open(image_file_1)
#open data from band 1 as numpy array 
df1 = ds1.GetRasterBand(1).ReadAsArray()

#open the image dataset
ds2 = gdal.Open(image_file_2)
#open data from band 1 as numpy array 
df2 = ds2.GetRasterBand(1).ReadAsArray()

#open the image dataset
ms = gdal.Open(mask_file)
#open data from band 1 as numpy array 
mf = ms.GetRasterBand(1).ReadAsArray()

#subset to mask area with data and flatten arrays 
df1 = df1[mf == 1]#subset to where mask equals 1
df1 = df1[df1 != 0]#subset to where is'nt 0 as no data value

df2 = df2[mf == 1]#subset to where mask equals 1
df2 = df2[df2 != 0]#subset to where is'nt 0 as no data value

#find regression stats for two variables
slope, intercept, r_value, p_value, std_err  = stats.linregress(df1, df2)

r_square = r_value**2

#print stats to terminal
print("r squared: "+str(r_square))
print("p value: "+str(p_value))
print("std error; "+str(std_err))

#basic plot 
#plot scatter with regression line 
plt.plot(df1, df2, 'o')
#add regression line based on slope and intercept calculated
plt.plot(df1, slope*df1 + intercept)
plt.show()
#plt.savefig(outfile, dpi = 300)

