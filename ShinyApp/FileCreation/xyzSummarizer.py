#!/usr/bin/python

# This python script will create the sum_xyz.js and sum_index.csv files needed to run the shinyApp.
   # To run this correctly, place this script in the same directory as the folder with a name given to dataFolder(see below), which should contain .sapt files containing the geometries of the molecules.
   # You can verify if the correct files are being read by looking in fileList.txt.

# THIS IS IMPORTANT: You must change the file names of the .sapt files so that molecules that are more than one word are connected by a hyphen, instead of an underscore.
   # (ex. dimethyl-ether, not dimethyl_ether). The program cannot differentiate when there are multiple underscores.

import os
dataFolder = 'Data'
fileList = 'fileList.txt'
sumXYZ = 'sum_xyz.js'
sumIndex = 'sum_index.csv'

# The processXYZ() function creates the files, and is run at the end.

def processXYZ(fileListName,sumXYZName,sumIndexName,dataFolderName):

    fileList = open(fileListName,'w')
    for filename in os.listdir(dataFolderName):
        if(str(filename)[0] != '.'):
            fileList.write(dataFolderName+"/"+str(filename))
            if (str(filename) != ""):
                fileList.write('\n')
    fileList.close()
    
    sumXYZ = open(sumXYZName,'w')
    sumIndex = open(sumIndexName,'w')
    sumIndex.write('first,last,m1,m2\n')
    index = 0
    
    for k,line in enumerate(open(fileListName,'r')):
        noExt = line.split('.')[0].split('/')[1]
        name = noExt.split('_')[0]+','+noExt.split('_')[1]
        inFile = open(line.rstrip('\n'),'r')
        sumIndex.write(str(index+1) + ',')
        if(k==0):
            sumXYZ.write('var geomDict = {\n')
        start = 0
        for p,line in enumerate(inFile):
                if((len(line.split()) == 1) and (start == 0)):
                        xyz = ""
                        i = 0
                        start = 1
                        index += 1
                        if((k!=0) or (p!=0)):
                            sumXYZ.write(",\n")
                        sumXYZ.write(str(index)+':')
                elif ((start ==1) and (len(line.split()) == 2)):
                        start = 0
                        sumXYZ.write("'" + str(i) + "\\n\\n" + xyz + "'")
                elif (len(line.split()) == 4):
                        for j, part in enumerate(line.split()):
                                if(j != 0):
                                    xyz += " " + part
                                else:
                                    xyz += part[0]
                                    if((len(part) > 1) and (part[1].islower())):
                                        xyz += part[1]
                        i += 1
                        xyz += "\\n"
        sumIndex.write(str(index) + ',' + name + '\n')
        inFile.close()
    sumXYZ.write("\n};")
    sumXYZ.close()
    sumIndex.close()

processXYZ(fileList,sumXYZ,sumIndex,dataFolder)
