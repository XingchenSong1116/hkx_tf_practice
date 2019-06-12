#coding:gbk
'''
Created on Jun 1, 2011

@author: Peter Harrington
'''
from numpy import *

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()] #strip()Ϊȥ���ո�
    datArr = [map(float,line) for line in stringArr] #line->float
    return mat(datArr) #��listת��Ϊmat

def pca(dataMat, topNfeat=9999999):
    meanVals = mean(dataMat, axis=0) #dataMat:N*D����ÿһ��Ϊһ��������ÿһ��Ϊһ������
    meanRemoved = dataMat - meanVals #remove mean,��numpy�����Զ��ǹ㲥��չά��
    covMat = cov(meanRemoved, rowvar=0) #covMat��ndarray
    eigVals,eigVects = linalg.eig(mat(covMat)) # inv(P)AP=Eig
    eigValInd = argsort(eigVals)            #sort, sort goes smallest to largest
    eigValInd = eigValInd[:-(topNfeat+1):-1]  #cut off unwanted dimensions,-1�����������
    redEigVects = eigVects[:,eigValInd]       #reorganize eig vects largest to smallest��ȡǰk����������,D*K,P_reduced=P(1:k)
    lowDDataMat = meanRemoved * redEigVects #transform data into new dimensions, X:n*D,�µ�ά���ݣ� y=X*P_reduced,ά��Ϊ��n*K
    reconMat = (lowDDataMat * redEigVects.T) + meanVals # x_hat=y*P.T+meanVals������ά����ת�ú����ƽ��ֵ
    return lowDDataMat, reconMat #��ά�ռ��е��źţ��ؽ�����ź�

def replaceNanWithMean(): 
    datMat = loadDataSet('secom.data', ' ') #1567�еĵ����ݣ�ÿ��������ά��
    numFeat = shape(datMat)[1] #����1567�����ݣ�590ά����
    for i in range(numFeat): #����ÿ��ά������nan�ģ���ȥ����Ȼ�������ֵ,datMat[:,i].A��ָ��ndarray��A1ָ����һά����
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i]) #values that are not NaN (a number),nonzero���ص�����������tuple,tuple���������й������±�
        datMat[nonzero(isnan(datMat[:,i].A))[0],i] = meanVal  #set NaN values to mean ����nan��Ϊ��ֵ�������е�����nan��ֵͬʱ��ΪmeanVal
    return datMat

if __name__=='__main__':
    print u'���� pca:\n'
    dataMat=loadDataSet('testSet.txt')
    lowDMat,reconMat=pca(dataMat,1) #�������ó�2���������Ƿ���ȷ
    print shape(lowDMat)
    import matplotlib
    import matplotlib.pyplot as plt 
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90) #
    ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red') #�ؽ�����źţ����ʹ���˽�ά����ô�ؽ�����ź���������
    plt.show()
    
    print u'���� replaceNanWithMean \n'
    dataMat=replaceNanWithMean()
    meanVals=mean(dataMat,axis=0);
    meanRemoved=dataMat-meanVals;
    covMat=cov(meanRemoved,rowvar=0); #590*590
    eigVals,eigVects=linalg.eig(mat(covMat)) #eigValsΪ����ֵ��eigVects����������
    print "end"
    
    
    