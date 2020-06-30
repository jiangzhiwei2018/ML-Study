
import numpy as np

def loadDataSet():
    postingList =[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not     #1代表侮辱性，0代表正常
    return postingList, classVec

def creatVocabList(dataSet):
    vocabSet=set([])
    for doc in dataSet:
        vocabSet=vocabSet|set(doc)  #合集的并集
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
        else:
            print("单词:%s 不在词汇表中"%word)
    return returnVec

def trainNB0(trainMat, trainCategory):
    docsLen=len(trainMat)
    lenWords=len(trainMat[0])
    pC_1=sum(trainCategory)/float(docsLen)  #计算class=1的概率  存在侮辱性的文档的概率
    pC_0=1-pC_1
    p0Num=np.ones(lenWords)   #创建一个维度和字数相等的0向量
    p1Num=np.ones(lenWords)   #创建一个维度和字数相等的0向量
    p0Denom=2.0
    p1Denom=2.0
    for i in range(docsLen):
        if trainCategory[i]==1:
            p1Num+=trainMat[i]
            p1Denom+=sum(trainMat[i])
        else:
            p0Num += trainMat[i]
            p0Denom += sum(trainMat[i])
    p1Vect=np.log(p1Num/p1Denom)
    p0Vect=np.log(p0Num/p0Denom)
    return p0Vect, p1Vect, pC_1

def classifyNB(vec2Classfy, p0Vec, p1Vec, pClass1):
    p1=sum(vec2Classfy*p1Vec)+np.log(pClass1)
    p0=sum(vec2Classfy*p0Vec)+np.log(1.0-pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOposts, listClasses = loadDataSet()
    myVocablict = creatVocabList(listOposts)
    trainMat = []
    for nowDoc in listOposts:
        trainMat.append(bagOfwords2VecMN(myVocablict, nowDoc))
    p0V, p1V, pAb=trainNB0(np.array(trainMat),np.array(listClasses))
    testEntry=['love','my','dalmation']
    thisDoc=np.array(bagOfwords2VecMN(myVocablict, testEntry))

    print(classifyNB(thisDoc, p0V, p1V, pAb))

    testEntry = ['stupid', 'garbage']
    thisDoc=np.array(bagOfwords2VecMN(myVocablict, testEntry))
    print(classifyNB(thisDoc, p0V, p1V, pAb))
    return 0

def bagOfwords2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print("单词:%s 不在词汇表中" % word)
    return returnVec

import re
from os import listdir

# def textParse(bigString):  # input is big string, #output is word list
#     #import re
#     listOfTokens = re.split('\W+', bigString)
#     return [tok.lower() for tok in listOfTokens if len(tok) > 0]
def textPares(bigString):
    #regEx = re.compile('\W+')
    strList=re.split('\W+',bigString)
    return [t.lower() for t in strList if len(t) > 0]
def spamTest():
    fileList1=listdir('email/spam')
    m1=len(fileList1)
    fileList2=listdir('email/ham')
    m2=len(fileList2)
    docList=[]
    fullText=[]
    classList=[]
    for i in range(m1):
        filameStr1=fileList1[i]
        filameStr2=fileList2[i]

        wordList1=textPares(open('email/spam/%s' %filameStr1).read())
        wordList2 = textPares(open('email/ham/%s' % filameStr2).read())

        docList.append(wordList1)
        fullText.extend(wordList1)
        classList.append(1)

        docList.append(wordList2)
        fullText.extend(wordList2)
        classList.append(0)
    vocabList=creatVocabList(docList)
    trainSet=list(range(50))
    testSet=[]
    for i in range(10):
        randIndex=int(np.random.uniform(0, len(trainSet)))
        testSet.append(trainSet[randIndex])
        del(trainSet[randIndex])
    trainMat=[]
    trainClass=[]
    for docIndex in trainSet:
        trainMat.append(bagOfwords2VecMN(vocabList, docList[docIndex]))
        trainClass.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB0(np.array(trainMat), np.array(trainClass))
    errorCont=0
    for docIndex in testSet:
        wordVect=np.array(bagOfwords2VecMN(vocabList,docList[docIndex]))
        if(classifyNB(wordVect,p0V,p1V,pSpam)!=classList[docIndex]):
            errorCont+=1
    errorRate=float(errorCont) / len(testSet)
    print("错误率为:", errorRate)
    return errorRate

# cnt=0.0
# for i in range(100):
#     cnt+=spamTest()
# print(cnt/100.0)

# def exmple2():
#     import feedparser
#     ny=feedparser.parse('http://www.reddit.com/r/python/.rss')
#     print(ny['entries'])
#     return 0

spamTest()






