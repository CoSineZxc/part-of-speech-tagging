import re
import numpy as np
from hmmlearn import hmm
import pickle
from fileop import InfoExct
from modelTest import modelUse
import random
import codecs
import sys


def TaggingString(strtest,modeldir):
    fr = open(modeldir, 'rb')
    model = pickle.load(fr)
    ObsvList = pickle.load(fr)
    StatesList = pickle.load(fr)
    fr.close()
    strslt=""
    strtest = re.split(u' ', strtest)
    SeenList = [[]]
    for i in strtest:
        if i in ObsvList:
            idx = ObsvList.index(i)
        else:
            idx = random.randint(0, len(ObsvList) - 1)
        SeenList[0].append(idx)
    SeenList = np.array(SeenList).T
    logprob, stalist = model.decode(SeenList, algorithm="viterbi")
    for i, t in enumerate(strtest):
        slt = t + '/' + StatesList[stalist[i]]+' '
        strslt+=slt
    return strslt


modeldir="./model/modelall.txt"
# strtest = "新华社 北京 １月 １５日 电 （ 记者 于 海生 ） 国务院 总理 李 鹏 今天 下午 在 人民 大会堂 会见 美国 所罗门美邦 公司 董事长 桑福·威尔 一行 时 说 ，"
# strrslt=TaggingString(strtest,modeldir)
# print(strrslt)


def Taggingfile(infiledir,modeldir,outfiledir):
    stalist=modelUse(modeldir,infiledir)
    strslt=""
    data=codecs.open(infiledir, "r", "gbk")
    data = re.split(u'[\r\n]', data.read())
    strtest=[]
    for i in data:
        i=re.split(u' ',i)
        strtest.append(i)
    num=0
    for i in strtest:
        if i==[]:
            continue
        for j in i:
            if j == '':
                continue
            slt=j+'/'+stalist[num]+' '
            strslt+=slt
            num+=1
        strslt+='\n'
    DataOut = codecs.open(outfiledir, "w", "gbk")
    DataOut.write(strslt)
    DataOut.close()
    print("Tagging Finished!")

infiledir=sys.argv[1]
outfiledir=sys.argv[2]

# Taggingfile("./data/TestInput.txt","./model/modelall.txt","./data/TestOutput.txt")
Taggingfile(infiledir,modeldir,outfiledir)