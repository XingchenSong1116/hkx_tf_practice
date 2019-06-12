# coding: gbk
'''
Created on Nov 28, 2010
Adaboost is short for Adaptive Boosting
@author: Peter
'''

from numpy import *

def loadSimpData():
    datMat = matrix([[ 1. ,  2.1],
        [ 2. ,  1.1],
        [ 1.3,  1. ],
        [ 1. ,  1. ],
        [ 2. ,  1. ]])
    classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datMat,classLabels

def loadDataSet(fileName):      #general function to parse tab -delimited floats,delimited:���ƣ������Ľ�
    numFeat = len(open(fileName).readline().split('\t')) #get number of fields 
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat-1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1])) #���һ��Ϊ����
    return dataMat,labelMat

#���ຯ��
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#just classify the data
    retArray = ones((shape(dataMatrix)[0],1)) #retArray:5*1,��ʼ��Ϊ+1
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:,dimen] > threshVal] = -1.0
    return retArray
    

def buildStump(dataArr,classLabels,D,*printOut):#DΪ�������������Ȩ��
    dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
    m,n = shape(dataMatrix)
    numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
    minError = inf #init error sum, to +infinity
    for i in range(n):#loop over all dimensions��������ά��ѭ��
        rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();#ȡ��ά�ϵ����ֵ����Сֵ
        stepSize = (rangeMax-rangeMin)/numSteps #�����ά�ϵĲ���
        for j in range(-1,int(numSteps)+1):#loop over all range in current dimension,��ά�ϸ���ֵ��
            for inequal in ['lt', 'gt']: #go over less than and greater than,�ڴ�ά�ϴ�ֵ���Ƚϴ��ں�С��
                threshVal = (rangeMin + float(j) * stepSize) #�õ��ָ����ֵ
                predictedVals = stumpClassify(dataMatrix,i,threshVal,inequal)#call stump classify with i, j, lessThan
                errArr = mat(ones((m,1)))
                errArr[predictedVals == labelMat] = 0 #��Ԥ��ֵ���ǩ��ͬ�ĵط�����Ԥ����ȷ����Ϊ0,�������ȻΪ1
                weightedError = D.T*errArr  #calc total error multiplied by D,�����ܵĴ���Ȩ��
                if printOut:
                    print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
                if weightedError < minError: #��¼���ֵ
                    minError = weightedError
                    bestClasEst = predictedVals.copy() #��õ�Ԥ����
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump,minError,bestClasEst


def adaBoostTrainDS(dataArr,classLabels,numIt=40,*printOut):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)   #init D to all equal,��ʼ��Ȩ��
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump,error,classEst = buildStump(dataArr,classLabels,D)#build Stump,ÿ��ѭ��ʱ�����������ݽ����ط��ֻ࣬�Ǵ�ʱ������Ȩ�ز�ͬ
        #print "D:",D.T
        alpha = float(0.5*log((1.0-error)/max(error,1e-16)))#calc alpha, throw in max(error,eps) to account for error=0������ԽС���÷�������Ȩ��alphaԽ��
        bestStump['alpha'] = alpha  #��¼Ȩ��
        weakClassArr.append(bestStump)                  #store Stump Params in Array,��list��¼��Щ������
        #print "classEst: ",classEst.T
        expon = multiply(-1*alpha*mat(classLabels).T,classEst) #exponent for D calc, getting messy, MultiplyΪ��Ԫ�����
        D = multiply(D,exp(expon))                              #Calc New D for next iteration, Adaboost�������Ȩ�صĹ�ʽ
        D = D/D.sum()
        #calc training error of all classifiers, if this is 0 quit for loop early (use break)
        aggClassEst += alpha*classEst #aggClassEst:Ϊ��¼ÿ�����ݵ��������ֵ
        #print "aggClassEst: ",aggClassEst.T
        aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1))) #ֻ������һ�µ����
        errorRate = aggErrors.sum()/m
        if printOut:
            print "total error: ",errorRate
        if errorRate == 0.0: break
    return weakClassArr,aggClassEst

def adaClassify(datToClass,classifierArr,*printOut):#adaboost�ķ��ຯ��
    dataMatrix = mat(datToClass)#do stuff similar to last aggClassEst in adaBoostTrainDS
    m = shape(dataMatrix)[0]
    aggClassEst = mat(zeros((m,1)))
    for i in range(len(classifierArr)):
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                 classifierArr[i]['thresh'],\
                                 classifierArr[i]['ineq'])#call stump classify
        aggClassEst += classifierArr[i]['alpha']*classEst  #Ȩ�س��Է����ǩ
        if printOut:
            print aggClassEst
    return sign(aggClassEst)

def plotROC(predStrengths, classLabels):#����ROC����,����Ԥ��ǿ��
    import matplotlib.pyplot as plt
    cur = (1.0,1.0) #cursor
    ySum = 0.0 #variable to calculate AUC
    numPosClas = sum(array(classLabels)==1.0) #��������
    yStep = 1/float(numPosClas);  #y����������������Ϊ����
    xStep = 1/float(len(classLabels)-numPosClas) #�Ը�����������Ϊ����
    sortedIndicies = predStrengths.argsort()#get sorted index, it's reverse
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    #loop through all the values, drawing a line segment at each point
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0: #��Ϊ�������������ʽ����޸�
            delX = 0; delY = yStep;
        else: #��Ϊ�������Լ����ʽ����޸�
            delX = xStep; delY = 0;
            ySum += cur[1]
        #draw line from cur to (cur[0]-delX,cur[1]-delY)
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b') #plot(x,y),ǰ����X�ᣬ������y��
        cur = (cur[0]-delX,cur[1]-delY) #���µ�ǰ���ֵ
    ax.plot([0,1],[0,1],'b--')
    plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
    plt.title('ROC curve for AdaBoost horse colic detection system')
    ax.axis([0,1,0,1])
    plt.show()
    print "the Area Under the Curve is: ",ySum*xStep


if __name__ == "__main__":
    print u"���������..."
    datMat,classLabels=loadSimpData()
    D=mat(ones((5,1))/5)
    bestStump,error,classEst =buildStump(datMat,classLabels,D)
    print u"���ž�����:"
    print bestStump,'\n',error,'\n',classEst 
    print u"AdaBoostѵ��..."
    classifierArr,aggClassEst=adaBoostTrainDS(datMat,classLabels,9,True)
    print u"AdaBoost����..."
    print adaClassify([0,0],classifierArr)
    print adaClassify([5,5],classifierArr)
    
    print u"�����޲����ݼ��ϲ���Adaboost�㷨..."
    datArr,labelArr=loadDataSet('horseColicTraining2.txt')
    trainErrArr=mat(ones((len(labelArr),1)))
    trainNum=10
    classifierArray,aggClassEst=adaBoostTrainDS(datArr,labelArr,trainNum)
    errcount=trainErrArr[sign(aggClassEst)!=mat(labelArr).T].sum()
    print u"ѵ������...��"
    print u"ѵ������",trainNum,"ѵ��������Ŀ",len(labelArr)," ������:",errcount,"�����ʣ�",errcount/len(labelArr)
    testArr,testLabelArr=loadDataSet('horseColicTest2.txt')
    prediction=adaClassify(testArr,classifierArray)
    errArr=mat(ones((len(testLabelArr),1)))
    errcount=errArr[prediction!=mat(testLabelArr).T].sum()
    print u"��������..."
    print u"����������Ŀ",len(testLabelArr)," ������:",errcount,"�����ʣ�",errcount/len(testLabelArr)
    
    print u"����ROC����..."
    plotROC(aggClassEst.T,labelArr)
    
