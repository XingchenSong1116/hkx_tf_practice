# -*- coding: gbk -*-
'''
Created on Oct 12, 2010
Decision Tree Source Code for Machine Learning in Action Ch. 3
@author: Peter Harrington
'''

from math import log
import operator

#�����򵥵ļ����㼯
def createDataSet():
    #   ��Ҫ����ˮ��ô��    �н���   ��������
    dataSet = [[1, 1, 'yes'], #����list
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    #        ��Ҫ����ˮ��ô��                 �н���
    labels = ['no surfacing','flippers'] # ����  ,list
    #change to discrete values
    return dataSet, labels

#��������ֵ����ũ��,��ʵֻ�����˱�ǩ����
def calcShannonEnt(dataSet):
    numEntries = len(dataSet) #�������ݼ�����������ʵ������
    labelCounts = {}
    for featVec in dataSet: #the the number of unique elements and their occurance
        currentLabel = featVec[-1]   #���һ��Ϊ��ǩ
        if currentLabel not in labelCounts.keys(): labelCounts[currentLabel] = 0 #�����ǰ��ǩ�������У�����Ϊ0
        labelCounts[currentLabel] += 1 #����ʹ��, classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1  #�����ǩ��ֵ�����ڣ�����0ΪĬ��ֵ
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries  #�������
        if prob!=0: #���Ϊ0�Ļ���ֱ������
            shannonEnt -= prob * log(prob,2) #log base 2
    return shannonEnt 

#���ո��������������ݼ�  ,���ӵ����ڸ�άaxis��ȡ��ֵvalue�Ĳ�������ά�������Ӽ�  
def splitDataSet(dataSet, axis, value):
    retDataSet = [] #�����µ�list����
    for featVec in dataSet: #featVecΪdataSet�е�ÿһ����list���ӵ�0����ʼ������list: [1, 1, 'yes']
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]     #chop out axis used for splitting,������axis
            reducedFeatVec.extend(featVec[axis+1:]) # �б�ɰ����κ��������͵�Ԫ�أ������б��е�Ԫ������ȫΪͬһ���͡� 
            #append�����������б��β�����һ���µ�Ԫ�ء�ֻ����һ��������
            #extend()����ֻ����һ���б���Ϊ�����������ò�����ÿ��Ԫ�ض���ӵ�ԭ�е��б��С�
            retDataSet.append(reducedFeatVec)
    return retDataSet

#ѡ����õ����������ݼ����л��֣�����Ϣ���������������л���    
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1      #the last column is used for the labels,���һ��Ϊ�����ǩ,��2������
    baseEntropy = calcShannonEnt(dataSet)  #�����ǩ����
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):        #iterate over all the features,������������
        featList = [example[i] for example in dataSet]#create a list of all the examples of this feature,featListΪ�������������и�ά��������ȡ,����������������������ȡֵ
        uniqueVals = set(featList)       #get a set of unique values,���Ͽ���ȥ���ظ�ֵ
        newEntropy = 0.0
        for value in uniqueVals: #��������ֵȡֵ�����
            subDataSet = splitDataSet(dataSet, i, value) #�ڸ�ά�϶����ݼ����л���,list: [[1, 'no'], [1, 'no']]
            prob = len(subDataSet)/float(len(dataSet)) #�����Ӽ�/��������
            newEntropy += prob * calcShannonEnt(subDataSet) #��������������ݼ���������    
        infoGain = baseEntropy - newEntropy     #calculate the info gain; ie reduction in entropy,������Ϣ����
        if (infoGain > bestInfoGain):       #compare this to the best gain so far
            bestInfoGain = infoGain         #if better than current best, set to best
            bestFeature = i  #������Ϣ������������
    return bestFeature                      #returns an integer
#�Ը����ݼ��г������ı�ǩ����ͳ�ƣ�����ǩ��
def majorityCnt(classList):
    classCount={} #���ǩ��,���������ֵ䣬�������б�
    for vote in classList: #���е����ǩ
        if vote not in classCount.keys(): classCount[vote] = 0 #�����ǩ��Ϊ��
        classCount[vote] += 1 #��ǩֵ��1������ñ�ǩ���ֵĴ���
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
#�������Ĵ���,����ֵ����Ϊ�ֵ�
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet] #��ȡ��������б�
    if classList.count(classList[0]) == len(classList): #����������ǩ����ͬ���򷵻ظñ�ǩ����yes�����ߡ�no������ֻ��һ��Ҷ���
        return classList[0]#stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1: #stop splitting when there are no more features in dataSet
        return majorityCnt(classList) #����ֻ��һά����ֻ�з����ǩ����û����������ֹͣ�ָ���������������
    bestFeat = chooseBestFeatureToSplit(dataSet) #ѡ����õ����������ݼ����л��֣�����Ϣ���������������л���    
    bestFeatLabel = labels[bestFeat] #��õ������ַ���:'no surfacing','flippters'
    myTree = {bestFeatLabel:{}} #�ֵ�
    del(labels[bestFeat]) #ɾ����������ǩ�ַ�������ֻʣ�¡�flippters��
    featValues = [example[bestFeat] for example in dataSet] #ȡ������������ά������ȡֵ
    uniqueVals = set(featValues) #ȥ��
    for value in uniqueVals: #��������ȡֵ����python�У�������Ϊ�б�����ʱ���ǰ������÷�ʽ���ݵģ�Ϊ�˱�֤ÿ�ε��ò��ı�ԭ�б����ݣ�����ʹ���±���sublabels����ԭʼ�б�
        subLabels = labels[:]       #copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value),subLabels)  #�ݹ����
    return myTree                            
#ʹ�þ������ķ��ຯ��    
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0] #no surfacing,��ȡ���ĸ���������
    secondDict = inputTree[firstStr]#ͨ��������ȡֵ,��ʵ�ǿ�����
    featIndex = featLabels.index(firstStr) #ͨ��inputTree����ȡ��������Ҫ�Ƚ���һ������
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: classLabel = valueOfFeat #�����Ҷ��㣬ֱ�ӷ���
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)
    
#������
dataset,labels=createDataSet()
print dataset
print labels
ent=calcShannonEnt(dataset)
print u"��:",ent

print u"���ո��������������ݼ�"
# print splitDataSet(dataset,0,1)
# print splitDataSet(dataset,0,0)

feature=chooseBestFeatureToSplit(dataset)
print u"best feature:",feature

print u"������"
myDat,labels=createDataSet()
myTree=createTree(myDat,labels)
print myTree
#dict: {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}

import treePlotter
# treePlotter.createPlot0()
myDat,labels=createDataSet()
myTree=treePlotter.retrieveTree(0)
print myTree
print classify(myTree,labels,[1,0])
print u"�洢��..."
storeTree(myTree,'classifierStorage.txt')
print u"��ȡ��..."
print grabTree('classifierStorage.txt')

print u"\n�����۾�:"
fr=open('lenses.txt')
lenses=[inst.strip().split('\t') for inst in fr.readlines() ]
lensesLabels=['age','prescript','astigmatic','tearRate']
lensesTree=createTree(lenses,lensesLabels)
print lensesTree

treePlotter.createPlot(lensesTree)




