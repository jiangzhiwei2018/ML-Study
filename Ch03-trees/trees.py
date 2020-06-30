from math import log
import pickle
import operator
import matplotlib.pyplot as plt

# http://en.wikipedia.org/wiki/ID3_algorithm ID3算法

def creatDataSet():
    dataSet=[[1,1,'yes'],
             [1,1,'yes'],
             [1,0,'no'],
             [0,1,'no'],
             [0,1,'no']]
    labbels=['no surfacing','flippers']
    return dataSet,labbels
    return 0

def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for fetVec in dataSet:
        currentLabel=fetVec[-1]
        #if currentLabel not in labelCounts:labelCounts[currentLabel]=0
        labelCounts[currentLabel]=labelCounts.get(currentLabel,0)+1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in  dataSet:
        if(featVec[axis]==value):
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numberFeatures=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numberFeatures):
        featList=[example[i] for example in dataSet]#取dataSet的第i列
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy +=prob*calcShannonEnt(subDataSet)
        nowInfo=baseEntropy-newEntropy
        if(nowInfo>bestInfoGain):
            bestInfoGain=nowInfo
            bestFeature=i
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        classCount[vote]=classCount.get(vote,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def creatTree(dataSet,labels):
    classList=[e[-1] for e in dataSet]

    if(len(dataSet[0])==1):
        return majorityCnt(classList)

    if(classList.count(classList[0])==len(classList)):
        return classList[0]
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestLabel=labels[bestFeat]
    resultTree={bestLabel:{}}
    del(labels[bestFeat])
    uniValue=set([e[bestFeat] for e in dataSet])
    for value in uniValue:
        subLabel=labels[:]
        newDataSet=splitDataSet(dataSet,bestFeat,value)
        resultTree[bestLabel][value]=creatTree(newDataSet,subLabel)

    # classList=[e[-1] for e in dataSet]
    # if(classList.count(classList[0])==len(classList)):
    #     return classList[0]
    # if(len(dataSet[0])==1):
    #     return majorityCnt(classList)
    # bestFeat=chooseBestFeatureToSplit(dataSet)
    # bestFeatLabels=labels[bestFeat]
    # myTree={bestFeatLabels:{}}
    # del(labels[bestFeat])
    # featValue=[e[bestFeat] for e in dataSet]
    # uniqueValue=set(featValue)
    # for value in uniqueValue:
    #     subLabels=labels[:]
    #     myTree[bestFeatLabels][value]=creatTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    # return myTree

    return resultTree

def classify(inputTree, featLabels, testVec):
    firstStr=list(inputTree.keys())[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] ==key:
            if type(secondDict[key])==dict:
                classLabel=classify(secondDict[key], featLabels, testVec)
            else: classLabel=secondDict[key]
    return classLabel

def myClassify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    index=featLabels.index(firstStr)

    for key in secondDict.keys():
        if testVec[index]==key:
            if type(secondDict[key])==dict:
                classLabel=myClassify(secondDict[key],featLabels,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw =open(filename,'wb+')
    pickle.dump(inputTree,fw)
    fw.close()
def grabTree(filename):
    import pickle
    fr=open(filename,'rb+')
    return pickle.load(fr)

def getExampleDataAndLabels(filename):
    fr=open(filename)
    lenses=[inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels=['age', 'prescript', 'astigmatic', 'tearRate']
    fr.close()
    return lenses,lensesLabels

# myDat, labels=creatDataSet()
# print(labels)
# mTree=creatTree(myDat,labels)
# print(mTree)
# myDat2,labels=creatDataSet()
# print(myClassify(mTree,labels, [1, 0]))

# storeTree(mTree,'classifierStorage.txt')
# print(grabTree('classifierStorage.txt'))

myDat,labels=getExampleDataAndLabels('lenses.txt')
print(myDat,labels)
mTree=creatTree(myDat,labels)
print(mTree)
import treePlotter as myTreePlot
myTreePlot.createPlot(mTree)

myDat2,labels=getExampleDataAndLabels('lenses.txt')
print(myClassify(mTree,labels,['young', 'myope', 'no', 'reduced']))