import re
import codecs
import pickle
import random
import numpy as np
import warnings

warnings.filterwarnings("ignore")


def LabelExct(dir):
    Labellist = []
    data = codecs.open(dir, "r", "gbk")
    data = re.split(u'[\r\n ]', data.read())
    for i in data:
        if i == '':
            continue
        i = i.split('/')
        Labellist.append(i[1])
    return Labellist


def modelUse(modeldir, Testdir):
    LabelList = []
    fr = open(modeldir, 'rb')
    model = pickle.load(fr)
    ObsvList = pickle.load(fr)
    StatesList = pickle.load(fr)
    fr.close()
    data = codecs.open(Testdir, "r", "gbk")
    data = re.split(u'[\r\n]', data.read())
    puncstr = ["，", "。", "、", "？", "；", "：", "“", "”", "‘", "’", "【", "】", "（", "）", "！"]
    data_new = []
    for i in data:
        headnum = 0
        for t, j in enumerate(i):
            if t == len(i) - 1:
                data_new.append(i[headnum:t + 1])
            elif j in puncstr:
                data_new.append(i[headnum:t + 1])
                headnum = t + 1
    for i in data_new:
        if i == '' or i == ' ':
            continue
        strtest = re.split(u' ', i)
        SeenList = [[]]
        for j in strtest:
            if j == "":
                continue
            if j in ObsvList:
                idx = ObsvList.index(j)
            else:
                idx = random.randint(0, len(ObsvList) - 1)
            SeenList[0].append(idx)
        SeenList = np.array(SeenList).T
        logprob, stalist = model.decode(SeenList, algorithm="viterbi")
        for j in stalist:
            LabelList.append(StatesList[j])
    return LabelList


def Rslt2Input(Rsltdir, Inputdir):
    DataIn = codecs.open(Rsltdir, "r", "gbk")
    DataOut = codecs.open(Inputdir, "w", "gbk")
    data = re.sub(u'1998....-..-...-.../m..', '', DataIn.read())
    data = re.sub(u'\[', '', data)
    data = re.sub(u'\]n.', '', data)
    data = re.sub(u'/\S{1,2}', '', data)
    data = re.sub(u' {2}', ' ', data)
    DataOut.write(data)
    DataOut.close()
    DataIn.close()


# Rslt2Input("./data/TestSetRslt.txt","./data/TestSetInput.txt")

def CalcAccy(Testdir, Labeldir, modeldir):
    Rslt2Input(Labeldir, Testdir)
    ModelLabelList = modelUse(modeldir, Testdir)
    TestSetList = []
    data = codecs.open(Labeldir, "r", "gbk")
    data = re.sub(u'1998....-..-...-.../m..', '', data.read())
    data = re.findall('(.)/(\S*)', data)
    for i in data:
        if ']' in i[1]:
            j = re.split(']', i[1])
            TestSetList.append(j[0])
        else:
            TestSetList.append(i[1])
    if len(ModelLabelList) == len(TestSetList):
        print("OK")
    else:
        print("mod:" + str(len(ModelLabelList)))
        print("Test:" + str(len(TestSetList)))
    RightNum = 0
    for i, j in enumerate(ModelLabelList):
        if j == TestSetList[i]:
            RightNum += 1
    accuracy = RightNum / len(ModelLabelList)
    return accuracy

# LabelExct('./data/test2.txt')

# ModelLabelList=modelUse("./model/modelall.txt","./data/TestSetInput.txt")

# acc = CalcAccy("./data/TestSetInput.txt", "./data/TestSetRslt.txt", "./model/modelall.txt")
# print(acc)
