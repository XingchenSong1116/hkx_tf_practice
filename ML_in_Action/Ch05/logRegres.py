# -*- coding: gbk -*-
'''
Created on Oct 27, 2010
Logistic Regression Working Module
@author: Peter
'''
from numpy import *

def loadDataSet():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])#�������б���Ԫ����ӵ�ԭ�б���
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)             #convert to NumPy matrix,100*3
    labelMat = mat(classLabels).transpose() #convert to NumPy matrix,100*1
    m,n = shape(dataMatrix)
    alpha = 0.001 #����
    maxCycles = 500 #��������
    weights = ones((n,1)) #��ʼȨ��,3*1
    for k in range(maxCycles):              #heavy on matrix operations
        h = sigmoid(dataMatrix*weights)     #matrix mult ,�������, 100*3,3*1
        error = (labelMat - h)              #vector subtraction
        weights = weights + alpha * dataMatrix.transpose()* error #matrix mult,3*100,100*1
    return weights

def plotBestFit(weights,_title='figure'):#�������ݼ��Լ��������
    import matplotlib.pyplot as plt
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0] 
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    plt.title(_title)
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s',label='positive')
    ax.scatter(xcord2, ycord2, s=30, c='green',label='negative')
    x = arange(-3.0, 3.0, 0.1) #��-3��3�����ݼ������в���Ϊ0.1
    y = (-weights[0]-weights[1]*x)/weights[2]  # w0+w1*x+w2*y=0
    y=array(y)
    x.shape=x.size,-1
    y.shape=x.size,-1
    
    ax.plot(x, y,c='black',label="line") #��ֱ֪��Ϊ�β�����ʾ
    plt.xlabel('X1'); plt.ylabel('X2');
    plt.legend()
    plt.show()

def stocGradAscent0(dataMatrix, classLabels):#����ݶ�����
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)   #initialize to all ones
    for i in range(m): #����������ѵ��һ��ͽ���
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = classLabels[i] - h
        weights = weights + alpha * error * array(dataMatrix[i])
    return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix) #m�д���m������
    weights = ones(n)   #initialize to all ones
    for j in range(numIter): #ѭ����������150��
        dataIndex = range(m)
        for i in range(m): #ÿһ�ε������ѡȡһ����������ѵ����ֱ����������ѵ�����
            alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not go to 0 because of the constant
            randIndex = int(random.uniform(0,len(dataIndex)))#���������
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h  #��ǩ-Ԥ��ֵ
            weights = weights + alpha * error * array(dataMatrix[randIndex])
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):#�ع���ຯ��
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest(iters):
    frTrain = open('horseColicTraining.txt'); frTest = open('horseColicTest.txt')
    trainingSet = []; trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):#0~20
            lineArr.append(float(currLine[i])) #�������б���Ԫ����ӵ�ԭ�б���
        trainingSet.append(lineArr) #���������ݼ�������
        trainingLabels.append(float(currLine[21])) #���һ��Ϊ���ǩ
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000) #����1000��
    errorCount = 0; numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print "��%d�Σ�the error rate of this test is: %f" %(iters+1,errorRate)
    return errorRate

def multiTest():#�������Ȼ����ȡƽ��ֵ
    numTests = 10; errorSum=0.0
    for k in range(numTests):
        errorSum += colicTest(k)
    print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))
 
print u"logistic�ع����"
dataArr,labelMat=loadDataSet()
weightsAsc=gradAscent(dataArr,labelMat)
print 'weights:',weightsAsc
# plotBestFit(weightsAsc,'gradAscent')


print u"����ݶ�����"
stocWeights=stocGradAscent0(dataArr,labelMat)
print 'stocWeights:',stocWeights
# plotBestFit(stocWeights,'stocGradAscent0')

print u"����ݶ�����,��˥��ϵ��"
stocWeights1=stocGradAscent1(dataArr,labelMat)
print 'stocWeights:',stocWeights1
# plotBestFit(stocWeights1,'stocGradAscent1')

print u"�������ǩ"
multiTest()
       