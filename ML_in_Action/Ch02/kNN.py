# -*- coding: gbk -*-
'''
Created on Sep 16, 2010
kNN: k Nearest Neighbors

Input:      inX: vector to compare to existing dataset (1xN)
            dataSet: size m data set of known vectors (NxM)
            labels: data set labels (1xM vector)
            k: number of neighbors to use for comparison (should be an odd number)
            
Output:     the most popular class label

@author: pbharrin
'''
from numpy import *
import operator
from os import listdir
import matplotlib
import matplotlib.pyplot as plt

    
#inXΪ�������������������������
#datssetΪ 4*2�У���4���㣬ÿ����Ϊ2ά
#labels��4����ǩ
#kΪ

#����ֻ������ٷ��������������ڵ������㣬�����ݺܶ�ʱ����ʹ��KD�������и�Ч�Ĳ���

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]    #����Ϊ4
    diffMat = tile(inX, (dataSetSize,1)) - dataSet #tile ��inx [0,0]����Ϊ4��1��
    sqDiffMat = diffMat**2  #��Ԫ��ƽ���������Ǿ������
    sqDistances = sqDiffMat.sum(axis=1) #���յ�1ά�������з��򣬴������ҽ�����ӣ�
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()  #��������   
    classCount={}          
    for i in range(k):#range(3)Ϊ 0,1,2,k=3,Ϊ3����
        voteIlabel = labels[sortedDistIndicies[i]] #ѡȡ��õ������������ı�ǩ
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1  #�����ǩ��ֵ�����ڣ�����0ΪĬ��ֵ
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True) #����2�����Խ�����������
    return sortedClassCount[0][0] #��������Ƶ���ı�ǩ��������

#���ɼ򵥵����ݼ�
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

#���ı���¼��ת��Numpy�Ľ�������
def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file���õ��ļ�����
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return���������ؾ���numpy
    classLabelVector = []                       #prepare labels return���������ر�ǩ   
    fr = open(filename)
    index = 0
    for line in fr.readlines():                 #readlines:һ�ζ�ȡ�ļ���������
        line = line.strip()                     #��ȡ�������лس���ո�
        listFromLine = line.split('\t')         #ԭ������tab���ָ�����ļ��к�����3���ո��
#         i=0
#         for x in listFromLine:
#             if x==' ':
#                 del listFromLine[i]          #ȥ�����еĿ�
#             i+=1
        
        returnMat[index,:] = listFromLine[0:3]  #����0��1��2��������3,��float�����ӣ�ֱ�ӽ�string listת���� float,��ȫ����numpy�����⴦��
        classLabelVector.append(int(listFromLine[-1]))  #���һ��Ϊ���ǩ,Ϊ����
        index += 1
    return returnMat,classLabelVector


#��ʾ����
def showData(dataSet,datingLabels):
#     plt.clf()
    fig=plt.figure()  
#     plt.ion()  #Switching interactive mode,�������Բ�������������
    ax=fig.add_subplot(111)
    ax.scatter(dataSet[:,1],dataSet[:,2],
               15.0*array(datingLabels),15.0*array(datingLabels))
    plt.xlabel("game time")
    plt.ylabel("ice cream")
#     plt.show(block=False) 
    plt.draw()  #�˴�ֻ����������ʾ
    
 
   
#��һ������ֵ    
def autoNorm(dataSet):
    minVals = dataSet.min(0)  #���Ÿ��У����ϵ�������Сֵ��n��3��
    maxVals = dataSet.max(0)  #
    ranges = maxVals - minVals  #���ֵ����Сֵ֮��
    normDataSet = zeros(shape(dataSet)) 
    m = dataSet.shape[0]  #numpy����,��þ��������
    normDataSet = dataSet - tile(minVals, (m,1))  #���н��и��ƣ�Ȼ�����
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide,���������
    return normDataSet, ranges, minVals   #���ع�һ�������ֵ����ֵ����Сֵ

#���Է�����Ч��   
def datingClassTest():
    hoRatio = 0.10      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load dataset from file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]  #����
    numTestVecs = int(m*hoRatio) #�������Ե�������
    errorCount = 0.0
    print "���ڽ��з���..."
    for i in range(numTestVecs):   #��i����Ϊ����           �ӵ�numTestVecs��ʼ�������Ϊ���ݿ�           3��3����
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0 #������󣬽����ۼ�
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount
#Ԥ�����  
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input(\
                                  "percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream, ]) #Ҳ��дΪarray([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - \
                                  minVals)/ranges, normMat, datingLabels, 3)  #��һ������ֵ
    print "You will probably like this person: %s" % resultList[classifierResult - 1]  
    
    
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32): #��32��
        lineStr = fr.readline() #ÿ��ֻ��ȡ�ļ���һ��
        for j in range(32): #��32��
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingClassTest():
    print "�������з���..."
    hwLabels = []  
    trainingFileList = listdir('trainingDigits')           #load the training set,listdir���Դ�ָ��Ŀ¼���г��ļ���
    m = len(trainingFileList)  #��ȡ�ļ��б�ĳ���
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr) #�����ǩ
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
        
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "%d:the classifier came back with: %d, the real answer is: %d" % (i+1,classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))
    print "�������..."


#print "begin debug"
# group,labels = createDataSet()
# classify0([0,0],group,labels,3 )
# datingDataMat,datingLabels =file2matrix('datingTestSet2.txt')
# normat,ranges,minvals=autoNorm(datingDataMat) #��һ������
# showData(normat,datingLabels)

# #����
# datingClassTest()
# plt.show()  #������show����ʾ����
# 
# #Ԥ��
# classifyPerson()

#��дʶ��
testVector=img2vector('testDigits/0_13.txt')
# print testVector[0,0:31]
# print testVector[0,32:63]

handwritingClassTest()
       