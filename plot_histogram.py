# !/usr/bin env python 

import gdal
import numpy as np 
import matplotlib.pyplot as plt

image_file = r"PATH TO FILE"
mask_file = r"PATH TO MASK"

#open the image dataset
ds = gdal.Open(image_file)
#open data from band 1 as numpy array 
df = ds.GetRasterBand(1).ReadAsArray()

#open mask dataset
ms = gdal.Open(mask_file)
#open data from band 1 as numpy array 
mf = ms.GetRasterBand(1).ReadAsArray()

#subset to the mask regions with data this will also flatten the array to 1d 
df = df[mf == 1]#subset to where mask equals 1
df = df[df != 0]#subset to where is'nt 0 as no data value

#plot histogram of different values from within data 

#define number of bins for histogram
#find total numbers of values
n = df.shape[0]
#find lower quartile
lq = np.percentile(df, 25)
#find upper quartile
uq = np.percentile(df, 75)
#find inter-quartile range
iqr = uq - lq
#define bin size
binSize = 2 * iqr * n**(-1/3)
#find number of bins based off bin size
numBins = int((np.max(df) - np.min(df))/binSize)+2
print("Number of bins in histogram: "+str(numBins))
#plot histogram of data using optomised bins
hist, bin_edges = np.histogram(df, bins=numBins)
center = (bin_edges[:-1] + bin_edges[1:]) / 2


#plot histogram
plt.bar(center, hist, align='center', width=binSize)
plt.show()
#plt.savefig(outfile, dpi = 300)
