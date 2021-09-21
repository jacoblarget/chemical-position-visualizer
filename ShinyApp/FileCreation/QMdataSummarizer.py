#!usr/bin/python

# This python script will create all of the energy.csv files needed for the shinyApp.
   # To run this correctly, place this script in the same directory as the folder with a name given to dataFolder(see below), which should contain a collection of folders, each containing .dat files.

import os
dataFolder = 'fit_exp_anisotropy'
var1List = ['anisotropic','fullisotropic','isotropic','scaledispanisotropic','scaledispfullisotropic','scaledispisotropic']
var2List = ['constrained','unconstrained']
QM = False

def processDataSet(dataFolder,var1List,var2List,QM):
    for var1 in var1List:
        for var2 in var2List:
            processData(dataFolder,var1,var2,QM)
    QM = True
    processData(dataFolder,var1,var2,QM)

def processData(dataFolder,var1,var2,QM):
    if(not QM):
        sumEnergyTypeName = 'sum_' + var1 + '_' + var2 + '_energy.csv'
    else:
        sumEnergyTypeName = 'sum_QM_energy.csv'
    sumEnergyType = open(sumEnergyTypeName, 'w')
    index = 0
    for folderName in os.listdir(dataFolder):
        if ((len(folderName.split('.')) == 1) and (folderName != 'old') and (folderName != 'save_figures') and (folderName !='input_templates') and (folderName != 'all_anisotropy_figures') and (folderName != 'foo')):
            bigList =[]
            processFolder(folderName,bigList,dataFolder,var1,var2,QM)
            for j in range(len(bigList[0])):
                if(index == 0):
                    sumEnergyType.write('index')
                elif(j!=0):
                    sumEnergyType.write(str(index))
                if(j!=0 or (j==0 and index==0)):
                    for list in bigList:
                        sumEnergyType.write(',' + list[j])
                    sumEnergyType.write('\n')
                    index += 1
    sumEnergyType.close()
        
def processFolder(folderName,bigList,dataFolder,var1,var2,QM):
    i = 0
    for fileName in os.listdir(dataFolder+'/'+folderName):
        if((fileName.split('_')[0] == var1) and (fileName.split('_')[-1] == var2 + '.dat')):
            processFile(fileName,bigList,i,folderName,dataFolder,QM)
            i += 1

def processFile(fileName,bigList,i,folderName,dataFolder,QM):    
    energyName = fileName.split('_')[3]
    if(len(fileName.split('_')) == 6):
        energyName += '_' + fileName.split('_')[4]
    bigList.append([energyName])
    file = open(dataFolder+'/'+folderName+'/'+fileName,'r')
    file.readline()
    for line in file:
        if (not QM):
            bigList[i].append(line.split()[1])
        else:
            bigList[i].append(line.split()[0])
    file.close()

processDataSet(dataFolder,var1List,var2List,QM)
