# -*- coding: gbk -*-
'''
Created on Oct 19, 2010

@author: Peter
'''
from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

          
def createVocabList(dataSet):#����һ�������������ĵ��г��ֵĲ��ظ��ʵ��б�       
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)
#���������ת��Ϊ�ʻ�����,�ʼ�ģ��
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList) #����Ϊ32�ļ����б���Ϊ����32������
    for word in inputSet:
        if word in vocabList: #����õ����ڴʻ���У���¼Ϊ1
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word  #�õ���δ���ʻ����¼������ʾ
    return returnVec #��������������ĵ�����

# ����ÿ�����ʵ����������ʣ�trainMatrix:Ϊ�ĵ�����trainCategory:Ϊ����ǩ
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix) #6���ĵ�����
    numWords = len(trainMatrix[0]) #�������ʵ�������32
    pAbusive = sum(trainCategory)/float(numTrainDocs) #�����ĵ��ĸ��ʣ�����ǩΪ1�Ľ�����Ӽ��ɵõ�
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones(),32�����ʵ�����������,��ʼ��Ϊ1����Ϊ��������˹ƽ��
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1: #����������
            p1Num += trainMatrix[i] #ͳ�����������иõ��ʳ��ֵĸ���
            p1Denom += sum(trainMatrix[i]) #���������г��ֵĵ�������
        else:  #������������
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)  #�����������У��õ��ʳ��ֵĸ��� ,log�������С����˵�������      #change to log()
    p0Vect = log(p0Num/p0Denom)  #�������Ե������У��õ��ʳ��ֵĸ���       #change to log()
    return p0Vect,p1Vect,pAbusive #�������������ʣ������

#vec2ClassifyΪ����������,
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult,��Ԫ�ص��,�˴���ӣ���ʵ�൱��log���������ˣ������ָ������ʵĸ�����˵õ����ӵĸ���
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else: 
        return 0
#�ʴ�ģ��,��ÿ�����ʽ��м���    
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1 #�����Ǽ�����1�������Ǽ򵥵���1
    return returnVec

#�������ر�Ҷ˹����
def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses)) #�õ������ʵ����������ʣ������
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString) #�ָ������������ʣ�����֮����ַ�
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] #���˵�����С��3���ַ�����������list
#�����ʼ�����    
def spamTest():
    docList=[]; classList = []; fullText =[]
    for i in range(1,26):#����26���ļ�
        wordList = textParse(open('email/spam/%d.txt' % i).read()) #�������ʼ�ת��Ϊ�ʻ��б�
        docList.append(wordList) #�������б���Ԫ����ӵ�ԭ�б���
        fullText.extend(wordList) #���б�������Ԫ�������ӵ��б��У�����δȥ�ظ�����
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read()) #���������ʼ�ת��Ϊ�ʻ��б�
        docList.append(wordList)
        fullText.extend(wordList) #append���б���ÿ��Ԫ�ض���ӵ�fullText��
        classList.append(0) #���һ����50�����ǩ
        ###
    vocabList = createVocabList(docList)#create vocabulary,�����ʻ��б�,ȥ���ظ�Ԫ��,����692��Ԫ��
    trainingSet = range(50); testSet=[]           #create test set,���������б�
    for i in range(10):  #�������ѡ��10���ı���Ϊ���Լ���1/5
        randIndex = int(random.uniform(0,len(trainingSet))) #��̬�ֲ�����0~50
        testSet.append(trainingSet[randIndex]) #���ı�����������Լ���
        del(trainingSet[randIndex])  #��ѵ������ɾ�����ı�����
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0, ��ѵ�����п�ʼѵ������
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))#���з���ѵ�������㵥�����������Լ������,arrayֱ�ӽ�listת��Ϊndarray
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:#���з��࣬�������������¼����
            errorCount += 1
            print "classification error",docList[docIndex] #�����������Ҫ���д�ӡԭ�ĵ�
    print 'the error rate is: ',float(errorCount)/len(testSet)
    #return vocabList,fullText
#��Ƶ��ȥ����������һЩͣ�ô�
def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True) 
    return sortedFreq[:30]    #ֻȡ ����Ƶ������0~29��  
#http://newyork.craigslist.org/stp/index.rss ���Է���
def localWords(feed1,feed0):
    import feedparser #feedparser��һ��RSS����������Դ�� https://code.google.com/p/feedparser/
    docList=[]; classList = []; fullText =[]
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary']) #ÿ�η���һ��rssԴ��������ת��Ϊ�ʵ��б�,����һ���ĵ�
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1) #NY is class 1
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)#create vocabulary,�Ѿ�������ȥ�ز���
    top30Words = calcMostFreq(vocabList,fullText)   #remove top 30 words,ȥ������Ƶ����ߵ�30������
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])
    trainingSet = range(2*minLen); testSet=[]           #create test set
    for i in range(20): #ѡ�����е�20��rssԴ���в���
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is: ',float(errorCount)/len(testSet)
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[]; topSF=[]
    for i in range(len(p0V)):
        if p0V[i] > -6.0 : topSF.append((vocabList[i],p0V[i])) #����������ʽϴ�����ΪԪ����뵽topSF��
        if p1V[i] > -6.0 : topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True) #lambda�У��Եڶ������Խ��бȽ�
    print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
    for item in sortedSF:
        print item[0],item[1]
    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
    for item in sortedNY:
        print item[0],item[1]

#test
list0Posts,listClasses= loadDataSet()
myVocabList=createVocabList(list0Posts)
print u"�ʻ��",myVocabList
vec1=setOfWords2Vec(myVocabList,list0Posts[0])
print vec1
vec2=setOfWords2Vec(myVocabList,list0Posts[3])
print vec2 
print u"######"
trainMat=[]
for postinDoc in list0Posts:
    trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
p0V,p1V,pAb=trainNB0(trainMat,listClasses)

print u"����������p0V��",p0V
print u"����������p1V��",p1V
print u"�����pAb��",pAb
print u"���� testingNB():"
testingNB()
print u"spamTest:"
spamTest()

print u"rss����"
import feedparser
ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
vocabList,pSF,pNy=localWords(ny,sf)

#getTopWords
getTopWords(ny,sf)

