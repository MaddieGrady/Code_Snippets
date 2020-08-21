
#!usr/bin env/python

import os.path
# Import the python sys module
import sys
# Import the python glob module
import glob
#  import the fnmatch module
import fnmatch
# Import the python Argument parser
import argparse
# Import os.walk to navigate directory structure.
import os

"""
    FUNCTION TO BUILD A SHELL SCRIPT TO SELECT AND EXTRACT REGIONS WHICH MEET CRITERIA IN SHAPEFILE
    
    call from command line
    
    see options at bottom of script
    
    """

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def buildCmds(InputPath, inputIsDIR, OutputFile, searchDepth, ColumnSelect, Condition, OutPath, NewOutName):
    InputPath = os.path.abspath(InputPath)
    OutputFile = os.path.abspath(OutputFile)
    
    Search = InputPath + "/*.shp"
    print(Search)
    InputFilesList = []
    for filename in find_files(InputPath, '*.shp'):
        InputFilesList.append(filename)
    print(InputFilesList)

if len(InputFilesList) == 0:
    raise Exception("No Input Files Specified. Check File Path")
    print(InputFilesList)
    
    outFile = open(OutputFile, 'w+')
    for File in InputFilesList:
        print("Processing :", File)
        if NewOutName == None:
            BaseName = os.path.splitext(os.path.split(File) [-1]) [0]
            print(BaseName)
            outfile = os.path.join(OutPath, BaseName + ".shp")
        else:
            outfile = os.path.join(OutPath, NewOutName + ".shp")
    
        cmd = 'ogr2ogr -f "ESRI Shapefile" ' + outfile
        
        if not ColumnSelect == None:
            cmd = cmd + " -select " + ColumnSelect

        if not Condition == None:
            cmd = cmd +' -where '+ Condition
        
        cmd = cmd + " " + File
        outFile.write(cmd + "\n")
    outFile.flush()
    outFile.close()



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='GenerateShellSciptToSelectShapefileRegions.py',
                                     description='''Command to build shell script to select and export shapefiles.''')
    parser.add_argument("-i", "--input", type=str, required=True,
                     help='''Input directory containing the data to be processed.''')
    parser.add_argument("-o", "--output", type=str, required=True,
                     help = '''Ouput location for shell script of commands''')
    parser.add_argument("-d", "--searchdepth", type =int, required=False, default = 1000,
                     help='''Depth of folders to search through for command''')
    parser.add_argument("-s", "--columnselect", type=str, required=False, default=None,
                     help = '''Names of columns to be included in output file''')
    parser.add_argument("-c", "--condition", type=str, required=False, default=None,
                     help = '''Condition to select from attribute table for new shapefile. Enter in SQL with appropriate formatting. REMEBER TO PUT '' AROUND THE COL NAME! AND NO SPACES!!''')
    parser.add_argument("-p", "--outfilespath", type=str, required = True,
                     help = '''path for output files in command''')
    parser.add_argument("-n", "--outname", type=str, required = False, default = None,
                     help = '''-new name for all output files, to use input name do not enter''')

    args = parser.parse_args()
                                     
    inputIsDIR = True

buildCmds(args.input, inputIsDIR, args.output, args.searchdepth, args.columnselect, args.condition, args.outfilespath, args.outname)


