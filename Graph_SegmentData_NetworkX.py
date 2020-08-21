
"""
    Create graph of connectivity and commoness of of image data using histogram and networkX - image data is provided
    as objects
    
    Designed to be performed on cloud masked data from ARCSII - removes cloud cover using mask regions
    
    INPUTS
    IMAGE DATA
    RASTER WITH ROI FOR NETWORKX e.g. Classification image
    OUTPUT FOLDER path for graph output
    
    Workflow
    1. Segment Image and Populate with Data
    2. Restrict Data to valid region
    3. Extract reflectance data from valid region and class in array
    4. Scale data to within range
    5. Bin data in histogram
    6. weighting based on frequency in nearby bins say 4 closest two smaller two larger
    7. start plotting network??
    """
#import required modules
import networkx as nx
import gdal
import rsgislib
import rios
from rios import rat
from rios import ratapplier
from rsgislib import rastergis
from rsgislib import imageutils
from rsgislib import imagecalc
from rsgislib import segmentation
from rsgislib.segmentation import segutils
from rsgislib.rastergis import ratutils
import numpy as np
import os
import sklearn
from sklearn import preprocessing
import matplotlib.pyplot as plt
from itertools import count
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial import distance
import operator

def SegAndValData(img, tmp, valid, baseclass):
    """
        Perform segmentation and generate mask of valid regions
        
        img = new optical/radar image for chagne analysis to be performed on
        tmp = tmp directory
        valid = file path for valid mask
        """
    #check if first processing has already been performed
    workingclumps = os.path.join(tmp, 'Clumps.kea')
    if os.path.exists(workingclumps)==False:
        #locate valid regions removing no data and then
        imagecalc.allBandsEqualTo(img, 1, 1, 0, valid, 'KEA', rsgislib.TYPE_16INT)
        #mask regions
        imageutils.maskImage(img, valid, os.path.join(tmp, 'ChangedDataImgage.kea'), 'KEA', rsgislib.TYPE_32FLOAT, 0, 1)
        #remove cloud cover areas using mask
        imagecalc.allBandsEqualTo(os.path.join(tmp, 'ChangedDataImgage.kea'), 0, 0, 1, valid, 'KEA', rsgislib.TYPE_16INT)
        rastergis.populateStats(valid, True, True)
        
        imagecalc.allBandsEqualTo(img, 1, 1, 0, os.path.join(tmp, 'tmpmask.kea'), 'KEA', rsgislib.TYPE_16INT)
        imageutils.maskImage(img, os.path.join(tmp, 'tmpmask.kea'), os.path.join(tmp, 'testimage.kea'), 'KEA', rsgislib.TYPE_32FLOAT, 0, 1)
        
        imagecalc.allBandsEqualTo(os.path.join(tmp, 'testimage.kea'), 0, 0, 1, valid, 'KEA', rsgislib.TYPE_16INT)
        rastergis.populateStats(valid, True, True)
        #run sheppard segmentation on image data
        
        segutils.runShepherdSegmentation(os.path.join(tmp, 'testimage.kea'),
                                         workingclumps,
                                         tmpath='./tmp',
                                         numClusters=60,
                                         minPxls=100,
                                         distThres=100,
                                         sampling=100, kmMaxIter=200)
        rastergis.populateStats(os.path.join(tmp, 'Clumps.kea'), True, True)
    
        rastergis.populateStats(workingclumps, True, True)
        #INPUT WITH NEW DATA
        #POPULATE WITH VALID, CLASSES FOR ROI EXTRACTION FOR NETWORKX,
        print("POPULATING RAT...")
        rastergis.populateRATWithMode(valid, workingclumps, 'Valid')
        rastergis.populateRATWithMode(baseclass, workingclumps, 'Class')
        #IMAGE DATA
        
        bs = []
        bs.append(rastergis.BandAttStats(band=2, meanField = 'BlueAvg'))
        bs.append(rastergis.BandAttStats(band=3, meanField = 'GreenAvg'))
        bs.append(rastergis.BandAttStats(band=4, meanField = 'RedAvg'))
        bs.append(rastergis.BandAttStats(band=7, meanField = 'NIRAvg'))
        bs.append(rastergis.BandAttStats(band=9, meanField = 'SWIR1Avg'))
        bs.append(rastergis.BandAttStats(band=10, meanField = 'SWIR2Avg'))
        rastergis.populateRATWithStats(img, workingclumps, bs)


    else:
        print("SEGMENTED IMAGE LOCATED...")

    return 'Class', workingclumps


def extractdata(img, inClassCol, classOfInterest, noDataVals, changeVarCol):
    """
        Function to extract data from a ROI val in a class and return it as an array.
        
        Extracted from classification functions in RSGISLib
        
        img = Clumps image with RAT to extract data from
        inClassCol = Class from which data will be restricted
        classOfInterest = the int for the ROI class
        nodatavals = no data to be removed from grid
        changeVarCol = list of columns which are to be used as varaibles for detecting chagne
        """
    # Open the image file...
    ratDataset = gdal.Open(img, gdal.GA_Update)
    ## Read in columns
    classVals = rat.readColumn(ratDataset, inClassCol)
    outChangeFeats = np.zeros_like(classVals)
    ID = np.arange(classVals.shape[0])
    vals = None
    numVars = len(changeVarCol)
    numRows = classVals.shape[0]
    varVals = np.zeros((numVars,numRows), dtype=np.int)
    i = 0
    for varCol in changeVarCol:
        colVals = rat.readColumn(ratDataset, varCol)
        varVals[i] = colVals
        i = i + 1
    varVals = varVals.transpose()
    ID = ID[classVals == classOfInterest]
    varVals = varVals[(classVals == classOfInterest)]
    ID = ID[np.isfinite(varVals).all(axis=1)]
    varVals = varVals[np.isfinite(varVals).all(axis=1)]
    for noDataVal in noDataVals:
        ID = ID[(varVals != noDataVal).all(axis=1)]
        varVals = varVals[(varVals != noDataVal).all(axis=1)]
    return varVals.transpose()

def SortHistogramNodes(frequency, bin_centers):
    """
        Remove instances with no examples of that node so as to reduce memory etc.
        frequency = 2d numpy array containing counts of data in each of the bins
        """
    count = 0
    nodes = dict()
    reducedfreq = []
    for y, i in zip(frequency, bin_centers):
        if sum(y) > 0.0:
            for x, j in zip(y, bin_centers):
                if x > 0.0:
                    nodes[count] = [i,j]
                    reducedfreq.append(x)
                    count+=1

    return nodes, reducedfreq

def StretchData(data):
    """
        Function to stretch each of the bands to cover the same range so that higher reflectance values dont become overaly weighted.
        """
    array = np.zeros_like(data, dtype = np.float)
    for a, i in zip(data, range(0, data.shape[1])):
        b = np.interp(a, (a.min(), a.max()), (0, 100))
        np.copyto(array[i], b)
    return(array)
def ClosestNodes(node, k):
    """
        Find K nearest nodes to create edges
        nodes = dictionary of node numbers and position in space
        k = number of nearby nodes to find
        """
    Connections = []#Create empty list object for tuples of nodes to connect
    for i in range(0, len(nodes)):#iterate to find the neighbours for each node
        node = nodes[i][0]#find the dictionary key for the node number, will need to be the first object in the connection tuple.
        distances = []#Create empty list for the distances of all the other points in the dataset
        for j in range(0, len(nodes)):#Iterate through the data set to measure euclidean distance
            dst = np.linalg.norm(np.asarray(nodes[i])-np.asarray(nodes[j]))#Find euclidean distance between the band data for each node
            #total = dst[0] + dst[1]
            if dst != 0.0:
                distances.append((j, dst))#append this distance to the dictionary of distances with the node number it relates to.
        distances.sort(key=operator.itemgetter(1))#sort the distances object based on the number produced for distance
        neighbournodes = []#create empty list object for the node number of the closest k nodes.
        for x in range(k):#limit to the range of k
            neighbournodes.append(distances[x][0])#append the node number to the list of closest nodes
        for n in neighbournodes:#iterate through neighbours to create tuples for edge create
            tuple = (i, n)#generate tuple from node numbers
            #print(tuple)
            Connections.append(tuple)#append to the list of all connections needed
    return Connections

def GraduateColoursNodeAttribute(Graph, Attribute):
    """
        Function to produce a colour map object based on a node attribute to be handed to the networkx draw function for nodes.
        Graph = the graph for which the colour is to be applied
        Attribute = string, the node attribute for which colour will be mapped
        """
    groups = set(nx.get_node_attributes(Graph,Attribute).values())
    mapping = dict(zip(sorted(groups),count()))
    node = Graph.nodes()
    colors = [mapping[Graph.node[n][Attribute]] for n in node]
    return colors
##################################################
##################INPUTS##########################
##################################################

img = 'filepath for image data'
baseclass = 'region of interest file'
tmp = 'tmp file path'

#IMAGE INFO FOR CREATING FILE PATHS AND PRINT TEXT ETC.
BaseName = os.path.splitext(os.path.split(img) [-1]) [0]
sensor = BaseName.split('_')[0]
date = BaseName.split('_')[1]
imginfo = sensor + "_" + date
print("IMAGE: "+imginfo)

#FILEPATHS FOR OUTPUT FILES
workingclumps = os.path.join(tmp, imginfo+"_WorkingClumps.kea")
valid = os.path.join(tmp, imginfo+"_Valid.kea")
stretchImage = os.path.join(tmp, imginfo+"_Stretched.kea")

#BEGIN PRE-PROCESSING
print("SEGMENTING IMAGE...")
#SEGMENT IMAGE AND VALID MASK
restrictedcol, workingclumps = segAndValData(img, tmp, valid, baseclass)
#EXTRACT DATA VALS
data = extractdata(workingclumps, restrictedcol, 1, [0], ['NIRAvg','SWIR1Avg'])
#STRETCH EACH BAND TO EQUAL RANGE
data = StretchData(data)

#BIN DATA INTO HISTOGRAM
frequency, bin_edgesx, bin_edgesy = np.histogram2d(data[0], data[1], bins = 50)
bin_centers = [i + 1 for i in bin_edgesx[:-1]]
#REMOVE UNNECESSARY BINS/NODES
nodes, frequency = SortHistogramNodes(frequency, bin_centers)

#CREATE EMPTY NETWORKX GRAPH SPACE
G  = nx.null_graph()
G.add_nodes_from(nodes)

#CREATE DICTIONARY CONNECTIONS FOR EDGES

Connections = ClosestNodes(nodes, 5)

#ADD EDGES FROM DICTIONARY
G.add_edges_from(Connections)


#ADD HISTOGRAM FREQUENCY AS ATTRIBUTE TO NODES
for f, i in zip(frequency, range(0, len(nodes))):
    G.nodes[i]['Frequency'] = f

#ADD CLUSTER METRIC AS ATTRIBUTE TO NODES
clustering = nx.square_clustering(G)
for node, cluster in clustering.items():
    G.nodes[node]['Clumping'] = cluster

#CENTRALITY
Closeness = nx.closeness_centrality(G)
for node, close in Closeness.items():
    G.nodes[node]['Closeness'] = close


#COLOUR NODES BY NODE ATTRIBUTE
#CHANGE ATTRIBUTE TO PLOT A DIFFERNET METRIC
colors = GraduateColoursNodeAttribute(G, 'Closeness')

#TRANSFER NODE INFORMATION TO MATPLOTLIB
nc = nx.draw_networkx_nodes(G, pos=nodes, nodelist=G.nodes(), node_color=colors,
                            with_labels=False, node_size=5, cmap=plt.cm.jet)
ne = nx.draw_networkx_edges(G, pos=nodes, width = 0.25)

#SHOW/SAVE MATPLOTLIB PLOT
plt.show()



G=nx.grid_2d_graph(4,4)  #4x4 grid

pos=nx.spring_layout(G,iterations=100)

plt.subplot(221)
nx.draw(G,pos,font_size=8)

plt.subplot(222)
nx.draw(G,pos,node_color='k',node_size=0,with_labels=False)

plt.subplot(223)
nx.draw(G,pos,node_color='g',node_size=250,with_labels=False,width=6)

plt.subplot(224)
H=G.to_directed()
nx.draw(H,pos,node_color='b',node_size=20,with_labels=False)

plt.savefig("outfile location")
plt.show()

