from numpy import *
from os import listdir
import operator
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def creatDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

#k-近邻
def classify0(inX, dataSet, labels, k):
    # inX     输入向量
    # dataSet 训练样本
    # labels  标签向量
    # k       最近邻居的数目
    dataSetSize = dataSet.shape[0]     # dataSet的行数
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet  # 通过tile把inX的单行向量扩展到和dataSet同样的行数，然后将inX与样本集中的每行做差，得到差矩阵（这是为了进行计算欧氏距离）
    sqDiffMat = diffMat ** 2         # 平方
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDisIndicies = distances.argsort()
    classCount = {}  #字典  key-value形式
    for i in range(k):
        voteIlabel=labels[sortedDisIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sorClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sorClassCount[0][0]

def file2matrix(filename):
    fr=open(filename)
    arrayLines=fr.readlines()
    numberOFline=len(arrayLines)
    returnMat=zeros((numberOFline,3))
    classLabelVector=[]
    index=0
    for line in arrayLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))# python中可用-1下标表示最后一列元素
        index+=1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minValue=dataSet.min(0)
    maxValue=dataSet.max(0)
    ranges=maxValue-minValue
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minValue,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minValue

def datingClassTest():
    hoRatio=0.10
    datingDataMat, datingLabels= file2matrix('Files/datingTestSet2.txt')
    norMat,ranges,minValue=autoNorm(datingDataMat)
    m=norMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(norMat[i,:],norMat[numTestVecs:m,:],
                                   datingLabels[numTestVecs:m],3)
        print("the classifier came back with : %d,the real answer is : %d"%(classifierResult,datingLabels[i]))
        if(classifierResult!=datingLabels[i]):
            errorCount+=1.0
    return (errorCount/float(numTestVecs))

def classifyPerson():
    resultList=['讨厌','一般喜欢','非常喜欢']
    percentTags=float(input("花多少时间玩游戏？"))
    ffmile=float(input("每年飞行多少公里？"))
    iceCream=float(input("每年冰淇淋的数量？"))
    datingMat,dataLabels=file2matrix('Files/datingTestSet2.txt')
    norMat,ranges,minVals=autoNorm(datingMat)
    inArr=array([ffmile,percentTags,iceCream])
    classifyResult=classify0((inArr-minVals)/ranges,norMat,dataLabels,3)
    return "你可能受喜欢的程度: ",resultList[classifyResult-1]

def img2vector(filename):
    returnVect=zeros((1,1024))
    fread=open(filename)
    for i in range(32):
        lineStr=fread.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return returnVect

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

    print("训练数据读取完毕，进入测试数据")

    testFileList = listdir('Files/digits/testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        print("第",i,"个")
        fileNameStr=testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumberStr = int(fileStr.split('_')[0])
        vectorUnderTest=img2vector('Files/digits/testDigits/%s'%fileNameStr)
        classifyResult=classify0(vectorUnderTest, trainMat, hwLabels, 3)
        if(classifyResult!=classNumberStr):errorCount+=1.0
    print("error rate is :%f"%(errorCount/float(mTest)))

    return errorCount/float(mTest)
print("-------------测试----------------")
#group, labels = creatDataSet()
#print(group, labels)
print("---------k-近邻算法----------------")
#print(classify0([3,1],group,labels,3))
print("---------kNN-examples----------------")
print(classifyPerson())
'''
datingDataMat,datingLabels=file2matrix('Files/datingTestSet2.txt')
print(datingDataMat,datingLabels)
norMat,ranges,minValue=autoNorm(datingDataMat)
print(norMat,ranges,minValue)
fig=plt.figure()
ax=fig.add_subplot(111) #1行1列 占第一块
ax.scatter(norMat[:,0],norMat[:,1],
           15.0*array(datingLabels),15.0*array(datingLabels))
plt.show()
'''
#testVector=img2vector('Files/digits/testDigits/0_3.txt')
#handwrittingClassTest()
