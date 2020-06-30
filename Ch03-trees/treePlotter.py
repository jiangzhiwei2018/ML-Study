import matplotlib.pyplot as plt
#import trees as mytr
decisionNode =dict(boxstyle="sawtooth",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

def createPlot(inTree):
    #plt.rcParams['font.sans-serif'] = ['simHei']

    fig=plt.figure(1, facecolor='white')
    fig.clf()

    axprops=dict(xticks=[], yticks=[])
    createPlot.ax1=plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree))
    plotTree.xOff=-0.5/plotTree.totalW
    plotTree.yOff=1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',\
                            xytext=centerPt, textcoords='axes fraction',\
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def getNumLeafs(myTrees):
    numLeafs=0
    firstStr=list(myTrees.keys())[0]
    secondDic=myTrees[firstStr]
    for key in secondDic.keys():
        if(type(secondDic[key])==dict):
            numLeafs+=getNumLeafs(secondDic[key])
        else: numLeafs +=1
    return numLeafs

def getTreeDepth(myTrees):
    maxDepth=0
    firstr=list(myTrees.keys())[0]
    secondDict=myTrees[firstr]
    for key in secondDict.keys():
        if(type(secondDict[key])==dict):
            thisDepth=1+getTreeDepth(secondDict[key])
        else: thisDepth=1
        if(thisDepth>maxDepth):
            maxDepth=thisDepth
    return maxDepth

def plotMidText(cntrPt, parentPt, txtString):
    xMid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

def plotTree(myTree, parentPt, nodeTxt):

    numLeafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=list(myTree.keys())[0]
    cntrpt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,
            plotTree.yOff)
    plotMidText(cntrpt,parentPt,nodeTxt)
    plotNode(firstStr, cntrpt, parentPt, decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff=plotTree.yOff-1.0/plotTree.totalD
    for key in secondDict.keys():
        if (type(secondDict[key])==dict):
            plotTree(secondDict[key], cntrpt, str(key))
        else:
            plotTree.xOff=plotTree.xOff+1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff,plotTree.yOff),
                     cntrpt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrpt, str(key))
    plotTree.yOff=plotTree.yOff+1.0/plotTree.totalD

    '''
    numLeafs = getNumLeafs(myTree)  # this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]  # the text label for this node should be this
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, 
              plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':  # test to see if the nodes are dictonaires, if not they are leaf nodes
            plotTree(secondDict[key], cntrPt, str(key))  # recursion
        else:  # it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), 
                     cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
    '''


# myDat, labels=mytr.creatDataSet()
# myTree=mytr.creatTree(myDat, labels)
#
# createPlot(myTree)
# myTree['no surfacing'][3]='maby'
# createPlot(myTree)
#
# print(dict)
# print(getNumLeafs(myTree))
# print(getTreeDepth(myTree))

