# coding:gbk
'''
Created on Jan 8, 2011

@author: Peter
'''
from numpy import *


def loadDataSet(fileName):      #general function to parse tab -delimited floats
    numFeat = len(open(fileName).readline().split('\t')) - 1 #get number of fields 
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr =[]
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws

def lwlr(testPoint,xArr,yArr,k=1.0):#testPointΪһ�����㣬lwlr��ͬ���ǣ�����ÿһ������һ�����Իع飬��ˣ�������е�Ļع�wϵ��������ͬ
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):                      #next 2 lines create weights matrix
        diffMat = testPoint - xMat[j,:]     #
        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws

def lwlrTest(testArr,xArr,yArr,k=1.0):  #loops over all the data points and applies lwlr to each one
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat

def lwlrTestPlot(xArr,yArr,k=1.0):  #same thing as lwlrTest except it sorts X first
    yHat = zeros(shape(yArr))       #easier for plotting
    xCopy = mat(xArr)
    xCopy.sort(0)
    for i in range(shape(xArr)[0]):
        yHat[i] = lwlr(xCopy[i],xArr,yArr,k)
    return yHat,xCopy

def rssError(yArr,yHatArr): #yArr and yHatArr both need to be arrays
    return ((yArr-yHatArr)**2).sum()

def ridgeRegres(xMat,yMat,lam=0.2):
    xTx = xMat.T*xMat
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = denom.I * (xMat.T*yMat)
    return ws
    
def ridgeTest(xArr,yArr):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0) #���ݱ�׼��,(x-mu)/sigma
    yMat = yMat - yMean     #to eliminate X0 take mean off of Y
    #regularize X's
    xMeans = mean(xMat,0)   #calc mean then subtract it off
    xVar = var(xMat,0)      #calc variance of Xi then divide by it
    xVar=sqrt(xVar) #��Ԫ�����ֵ
    xMat = (xMat - xMeans)/(xVar+1e-10) #python���Զ�����repmatά��,���Ǵ˴���xVarӦΪxVar**0.5�Ŷ�
    numTestPts = 30 #lambda����
    wMat = zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T #��lambda=exp(i)ʱ���洢��ǰϵ������i��
    return wMat

def regularize(xMat):#regularize by columns
    inMat = xMat.copy()
    inMeans = mean(inMat,0)   #calc mean then subtract it off
    inVar = var(inMat,0)      #calc variance of Xi then divide by it
    inMat = (inMat - inMeans)/sqrt(inVar)
    return inMat

#ǰ�������Իع�
def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean     #can also regularize ys but will get smaller coef
    xMat = regularize(xMat)
    m,n=shape(xMat) #m��������n������
    returnMat = zeros((numIt,n)) #testing code remove
    ws = zeros((n,1)); wsTest = ws.copy(); wsMax = ws.copy()
    for i in range(numIt):#ÿ�ֵ���
        #print ws.T
        lowestError = inf; 
        for j in range(n):#ÿ������
            for sign in [-1,1]:#������С
                wsTest = ws.copy()
                wsTest[j] += eps*sign #ÿ������Ȩ��ϵ������С�Ķ�
                yTest = xMat*wsTest  # ���¼���Ȩֵ
                rssE = rssError(yMat.A,yTest.A)
                if rssE < lowestError: #����̰�Ĳ��ԣ����ȵ�ǰС������м�¼
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy() #�ڴ��ֵ����У�ÿ��������������С�Ŷ�����¼�Ŷ������С���ϵ��
        returnMat[i,:]=ws.T #��i�м�¼��ѵ�Ȩ��ϵ��
    return returnMat

#def scrapePage(inFile,outFile,yr,numPce,origPrc):
#    from BeautifulSoup import BeautifulSoup
#    fr = open(inFile); fw=open(outFile,'a') #a is append mode writing
#    soup = BeautifulSoup(fr.read())
#    i=1
#    currentRow = soup.findAll('table', r="%d" % i)
#    while(len(currentRow)!=0):
#        title = currentRow[0].findAll('a')[1].text
#        lwrTitle = title.lower()
#        if (lwrTitle.find('new') > -1) or (lwrTitle.find('nisb') > -1):
#            newFlag = 1.0
#        else:
#            newFlag = 0.0
#        soldUnicde = currentRow[0].findAll('td')[3].findAll('span')
#        if len(soldUnicde)==0:
#            print "item #%d did not sell" % i
#        else:
#            soldPrice = currentRow[0].findAll('td')[4]
#            priceStr = soldPrice.text
#            priceStr = priceStr.replace('$','') #strips out $
#            priceStr = priceStr.replace(',','') #strips out ,
#            if len(soldPrice)>1:
#                priceStr = priceStr.replace('Free shipping', '') #strips out Free Shipping
#            print "%s\t%d\t%s" % (priceStr,newFlag,title)
#            fw.write("%d\t%d\t%d\t%f\t%s\n" % (yr,numPce,newFlag,origPrc,priceStr))
#        i += 1
#        currentRow = soup.findAll('table', r="%d" % i)
#    fw.close()
    
from time import sleep
import json
import urllib2
def searchForSet(retX, retY, setNum, yr, numPce, origPrc):#��google�ϻ�ȡ������Ϣ
    sleep(10)
    myAPIstr = 'AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY'
    searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)
    pg = urllib2.urlopen(searchURL)
    retDict = json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem = retDict['items'][i]
            if currItem['product']['condition'] == 'new':
                newFlag = 1
            else: newFlag = 0
            listOfInv = currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice = item['price']
                if  sellingPrice > origPrc * 0.5:
                    print "%d\t%d\t%d\t%f\t%f" % (yr,numPce,newFlag,origPrc, sellingPrice)
                    retX.append([yr, numPce, newFlag, origPrc])
                    retY.append(sellingPrice)
        except: print 'problem with item %d' % i
    
def setDataCollect(retX, retY):
    searchForSet(retX, retY, 8288, 2006, 800, 49.99)
    searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
    searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
    searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
    searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
    searchForSet(retX, retY, 10196, 2009, 3263, 249.99)
    
def crossValidation(xArr,yArr,numVal=10):#������֤���ԣ���ѡȡ���ŵ���ع��е�lambdaϵ��
    m = len(yArr)  #  ��Ʒ��Ŀ                      
    indexList = range(m)
    errorMat = zeros((numVal,30))#create error mat 30columns numVal rows
    for i in range(numVal):#10�۽�����֤
        trainX=[]; trainY=[]
        testX = []; testY = []
        random.shuffle(indexList) #�����ݽ��л�ϴ
        for j in range(m):#create training set based on first 90% of values in indexList
            if j < m*0.9: #ѵ����
                trainX.append([x for x in xArr[indexList[j]].A1])
                trainY.append(yArr[indexList[j]])
            else:#���Լ�
                testX.append([x for x in xArr[indexList[j]].A1])
                testY.append(yArr[indexList[j]])
        wMat = ridgeTest(trainX,trainY)    #get 30 weight vectors from ridge,
        #wMat[i,:]����lambda=e^iʱ��ϵ��
        for k in range(30):#loop over all of the ridge estimates
            matTestX = mat(testX); matTrainX=mat(trainX)
            meanTrain = mean(matTrainX,0)
            varTrain = var(matTrainX,0)+1e-10
            matTestX = (matTestX-meanTrain)/varTrain #regularize test with training params
            yEst = matTestX * mat(wMat[k,:]).T + mean(trainY)#test ridge results and store
            errorMat[i,k]=rssError(yEst.T.A,array(testY)) #��i����֤�У�lambda=e^iʱ�����
            #print errorMat[i,k]
    meanErrors = mean(errorMat,0)#calc avg performance of the different ridge weight vectors
    minMean = float(min(meanErrors)) #ѡȡ�����С��lambda
    bestWeights = wMat[nonzero(meanErrors==minMean)]#�����һ��ѵ����ϵ����Ϊ��׼,ʵ����һ�������ô�lambda�����������ݼ���ѵ��һ�εõ�W
    #can unregularize to get model
    #when we regularized we wrote Xreg = (x-meanX)/var(x),ymat=Xreg*wreg
    #we can now write in terms of x not Xreg:  x*w/var(x) - meanX/var(x) +meanY
    xMat = mat(xArr); yMat=mat(yArr).T
    meanX = mean(xMat,0); varX = sqrt(var(xMat,0)+1e-10)
    unReg = bestWeights/varX  #��ϵ��ȥ��һ��
    ind=nonzero(meanErrors==minMean)[0] #nonZero�����±�
    print "the best lambda:\n",exp(ind-10)
    print "the best model from Ridge Regression is:\n",unReg
    print "with constant term: ",-1*sum(multiply(meanX,unReg)) + mean(yMat)
 
if __name__ == "__main__":
    print u"�������Իع�..."
    xArr,yArr=loadDataSet('ex0.txt')
    #xArr[0:2]
    ws=standRegres(xArr,yArr)
    xMat=mat(xArr)
    yMat=mat(yArr)
    yHat=xMat*ws
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0])
    xCopy=xMat.copy()
    xCopy.sort(0)
    yHat=xCopy*ws
    ax.plot(xCopy[:,1],yHat)
    #plt.show()
    
    print u"���Ծֲ���Ȩ���Իع�..."
    xArr,yArr=loadDataSet('ex0.txt')
    yHat=lwlrTest(xArr,xArr,yArr,0.003)
    
    
    print u"�ڱ��㼯�ϲ�����ع�..."
    abX,abY=loadDataSet('abalone.txt')
    ridgeWeights=ridgeTest(abX, abY)
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(ridgeWeights)
    plt.rcParams['font.sans-serif'] = ['SimHei'] #ָ��Ĭ������  
    plt.rcParams['axes.unicode_minus'] = False #�������ͼ���Ǹ���'-'��ʾΪ���������  
    plt.xlabel('log(lambda)'); plt.ylabel('ridgeWeights')
    plt.title(u"��lambda����ʱ�������ϵ������0")
    
        
    print u"����ǰ���𲽻ع飨��lasso��⣩..."    
    xArr,yArr=loadDataSet('abalone.txt')
    bestWeights=stageWise(xArr,yArr,0.01,500)
    print bestWeights
    
    
    print u"�ָ߹���۸�Ԥ��..." 
    xArr,yArr=loadDataSet('abalone.txt')
    shp=shape(xArr)
    lgX=mat(ones((shp[0],shp[1]+1))) #��ȫ1���ڵ�һ��,��ΪX0=1
    lgX[:,1:shp[1]+1]=mat(xArr)
    lgY=yArr
    #setDataCollect(lgX,lgY)
    crossValidation(lgX,lgY,10) #������֤������ع�
    
    
    
    plt.show()#��Զ������󣬷�����������������