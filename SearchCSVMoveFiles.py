"""
    search a csv file of identifiers e.g. tile names and move matching files to a seperate folder
    version one searches whole file name for identifier
    version two can be used to restrict to a relevant section
    """
#import required modules
import glob
import os
import csv


############
#Version 1 #
############
with open("csv_list.csv") as f:
    reader = csv.reader
    data = list(reader)

#if required remove empty brackets around data
data = data[0]
for i in data:
    search_folder = glob.glob("folder of image to extract from"+"*.tif")
    #if required restrict to identifier section of filename e.g. tile
    for j in search_folder:
        if i in j:
            filename = os.path.split(j)[-1]
            os.rename(j, os.path.join("new output location", filename))

###########
#Version 2#
###########
with open("csv_list.csv") as f:
    reader = csv.reader
    data = list(reader)

#if required remove empty brackets around data
data = data[0]
for i in data:
    search_folder = glob.glob("folder of image to extract from"+"*.tif")
    search_subset = [os.path.split(k).split('.')[0].split('_')[1] for k in search_folder]
    #if required restrict to identifier section of filename e.g. tile
    for j, m in zip(search_folder, search_subset):
        if i == m:
            filename = os.path.split(j)[-1]
            os.rename(j, os.path.join("new output location", filename))
