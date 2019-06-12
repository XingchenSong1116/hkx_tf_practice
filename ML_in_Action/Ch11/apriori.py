#coding:gbk
'''
Created on Mar 24, 2011
Ch 11 code
@author: Peter
'''
from numpy import *

def loadDataSet():
    return [[1, 3, 4],
            [2, 3, 5], 
            [1, 2, 3, 5], 
            [2, 5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
                
    C1.sort()
    return map(frozenset, C1)#use frozen set so we
                            #can use it as a key in a dict    

def scanD(D, Ck, minSupport):#DΪ�����б��ϣ�CkΪ���б�,
    ssCnt = {} #�ֵ�
    for tid in D: #��ÿ������
        for can in Ck:#����ÿ������
            if can.issubset(tid):#������������������
                if not ssCnt.has_key(can): ssCnt[can]=1 #�õ���û�б����������м���
                else: ssCnt[can] += 1
               
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:#����L1Ƶ���
        support = ssCnt[key]/numItems #���㵥���֧�ֶ�
        if support >= minSupport:
            retList.insert(0,key) #����Ƶ��1�
            if support >=1:
                support=support
        supportData[key] = support #��¼֧�ֶ�,������������Ƶ����
    return retList, supportData
#����Ƶ��L(k-1)���������ѡk�
def aprioriGen(Lk, k): #creates Ck,���ɺ�ѡk�,����ʵ�ֵķ�����û����������֪ʶ���м�֦
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): #jΪi�ĺ�һ��
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()#���ɺ�ѡk���ǰk-2��϶�Ҫ��ͬ
            if L1==L2: #if first k-2 elements are equal
                #kexin Hu����Apriori�еļ�֦����
                un=Lk[i]|Lk[j]
                flag=True #����ΪƵ��
                unList=list(un) #�õ�un�ĸ���list
                for ri in range(k):
                    item=unList.pop(ri) #���μ��k-1��Ƿ�Ƶ��
                    if frozenset(unList) not in Lk:#��֤��ÿ���Ӽ�������Ƶ����
                        flag=False
                        break
                    unList.insert(ri,item)  #�ָ�ԭ����list
                if flag and un not in retList:
                    retList.append(un) #set union,ʾ��������{1,2}U{1,3}=>{1,2,3},��Ϊ����ǰ1����ͬ
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)#1��ѡ�
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):#L[k-2]:��ʵΪ�ո���ӽ�ȥ���
        Ck = aprioriGen(L[k-2], k) #���ɺ�ѡk�
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk,ɨ�������񼯣�ȥ������Ҫ��ĺ�ѡ����õ�Ƶ��k�
        supportData.update(supK) #����֧�ֶȼ�������ʵ�����
        L.append(Lk) #lk���ӵ�ԭ�б�
        k += 1
    return L, supportData
#���ɹ�������,LΪƵ���
def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items,�����ٺ�����������ʼ
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet] #�õ�Lk��е�ÿһ��,H��Ϊ������
            if (i > 1):#Lk����������3��
#                 if set(freqSet)==set([2,3,5]):
#                     print 'x'
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:#Lk����ֻ������������Ŷ�
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList         

def calcConf(freqSet, H, supportData, brl, minConf=0.7):#�������Ŷ�
    prunedH = [] #create new list to return
    for conseq in H: #H������Ϊ������
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence���������Ŷ�
#         if set(freqSet)==set([2,3,5]):
#             print 'x'
        if conf >= minConf: 
            print freqSet-conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq, conseq, conf)) #��¼����
            prunedH.append(conseq) #��¼���
    return prunedH #���غ���б�

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0]) #�õ���������Ԫ�ظ���
    if (len(freqSet) > (m + 1)): #try further merging,��Ƶ�����Ԫ�رȹ�����������2������кϲ�
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates,��Ƶ��m������ɺ�ѡm+1�
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
            
def pntRules(ruleList, itemMeaning):
    for ruleTup in ruleList:
        for item in ruleTup[0]:
            print itemMeaning[item]
        print "           -------->"
        for item in ruleTup[1]:
            print itemMeaning[item]
        print "confidence: %f" % ruleTup[2]
        print       #print a blank line

from time import sleep        
'''            
from votesmart import votesmart
votesmart.apikey = 'a7fa40adec6f4a77178799fae4441030'
#votesmart.apikey = 'get your api key first'
def getActionIds():
    actionIdList = []; billTitleList = []
    fr = open('recent20bills.txt') 
    for line in fr.readlines():
        billNum = int(line.split('\t')[0])
        try:
            billDetail = votesmart.votes.getBill(billNum) #api call
            for action in billDetail.actions:
                if action.level == 'House' and \
                (action.stage == 'Passage' or action.stage == 'Amendment Vote'):
                    actionId = int(action.actionId)
                    print 'bill: %d has actionId: %d' % (billNum, actionId)
                    actionIdList.append(actionId)
                    billTitleList.append(line.strip().split('\t')[1])
        except:
            print "problem getting bill %d" % billNum
        sleep(1)                                      #delay to be polite
    return actionIdList, billTitleList

                
def getTransList(actionIdList, billTitleList): #this will return a list of lists containing ints
    itemMeaning = ['Republican', 'Democratic']#list of what each item stands for
    for billTitle in billTitleList:#fill up itemMeaning list
        itemMeaning.append('%s -- Nay' % billTitle)
        itemMeaning.append('%s -- Yea' % billTitle)
    transDict = {}#list of items in each transaction (politician) 
    voteCount = 2
    for actionId in actionIdList:
        sleep(3)
        print 'getting votes for actionId: %d' % actionId
        try:
            voteList = votesmart.votes.getBillActionVotes(actionId)
            for vote in voteList:
                if not transDict.has_key(vote.candidateName): 
                    transDict[vote.candidateName] = []
                    if vote.officeParties == 'Democratic':
                        transDict[vote.candidateName].append(1)
                    elif vote.officeParties == 'Republican':
                        transDict[vote.candidateName].append(0)
                if vote.action == 'Nay':
                    transDict[vote.candidateName].append(voteCount)
                elif vote.action == 'Yea':
                    transDict[vote.candidateName].append(voteCount + 1)
        except: 
            print "problem getting actionId: %d" % actionId
        voteCount += 2
    return transDict, itemMeaning
'''

if __name__=='__main__':
    print u"����Apriori�㷨:"
    dataSet=loadDataSet()
    C1=createC1(dataSet)
    print u"C1\n",C1
    '''
    D=map(set,dataSet)
    L1,suppData0=scanD(D,C1,0.5)
    print u"L1\n",L1,u"\nsuppData0\n",suppData0
    '''
    L,suppData=apriori(dataSet,0.5)
    print u"\nL:\n",L,"\nsuppData:\n",suppData
    
    print u"���ɹ�������"
    rules=generateRules(L,suppData,minConf=0.5)
    print u"rules:\n",rules
    
    print u"��Ģ������..."
    mushDatSet=[line.split() for line in open('mushroom.dat').readlines()]
    L,suppData=apriori(mushDatSet,minSupport=0.4)
    for item in L[3]:
        if item.intersection('2'):#2�����ж�
            print item
            
    print u"����"