from numpy import *
from os import listdir
import operator
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def img2vector(filename):
    returnVect=zeros((1,1024))
    fread=open(filename)
    for i in range(32):
        lineStr=fread.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return returnVect
testVector=img2vector('Files/digits/testDigits/0_3.txt')

def handwrittingClassTest():
    hwLabels=[]
    trainFileList=listdir('Files/digits/trainingDigits')
    m=len(trainFileList)
    trainMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumberStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumberStr)
        trainMat[i,:]=img2vector('Files/digits/trainingDigits/%s'%fileNameStr)

print(testVector)
