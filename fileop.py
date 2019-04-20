import re
import codecs
import numpy as np
import gc

'''
函数名称：InfoExct
输入参数：dir：文件路径
输出参数：HMM五元组
函数功能：从语料文本中提取HMM五元组
'''


def InfoExct(dir):
    # HMM五元组
    StatesList = []
    ObsvList = []
    OrglStateProb = np.array([])
    TransProb = []
    EmissProb = []
    # 计算五元组基本元素
    num_stateforO = {}
    num_stateforS = {}
    num_S2S = {}
    num_S2O = {}
    num_SHead = {}
    data = codecs.open(dir, "r", "gbk")
    # 将语料按行拆分
    data = re.split(u'[\r\n]', data.read())
    data = np.array(data)
    data_new = np.array([])
    for i in data:
        if i == '':
            continue
        LineElemt = {}
        dataline = re.split(u' {2}', i)
        for t, j in enumerate(dataline):
            if j == '':
                continue
            j = re.split('/', j)
            if j[0].find('[') != -1:
                LineElemt[j[0][1:]] = j[1]
            elif j[1].find(']') != -1:
                LineElemt[j[0]] = j[1][:j[1].find(']')]
            else:
                LineElemt[j[0]] = j[1]
            if j[1][0] == 'w':
                data_new = np.append(data_new, LineElemt)
                LineElemt = {}
        if LineElemt != {}:
            data_new = np.append(data_new, LineElemt)
    del data
    gc.collect()
    for i in data_new:
        pre = ''
        skip = False
        for t, j in enumerate(i):
            if j not in ObsvList:
                ObsvList.append(j)
            if i[j] not in num_stateforO:
                StatesList.append(i[j])
                num_stateforO[i[j]] = 1
            else:
                num_stateforO[i[j]] += 1
            if i[j] not in num_S2O:
                num_S2O[i[j]] = {j: 1}
            elif j not in num_S2O[i[j]]:
                num_S2O[i[j]][j] = 1
            else:
                num_S2O[i[j]][j] += 1
            if t == 0:
                if re.search('1998', j) != None:
                    skip = True
                    continue
                pre = i[j]
                if pre not in num_stateforS:
                    num_stateforS[pre] = 1
                else:
                    num_stateforS[pre] += 1
                if i[j] not in num_SHead:
                    num_SHead[i[j]] = 1
                else:
                    num_SHead[i[j]] += 1
            elif skip == True:
                pre = i[j]
                if pre not in num_stateforS:
                    num_stateforS[pre] = 1
                else:
                    num_stateforS[pre] += 1
                if i[j] not in num_SHead:
                    num_SHead[i[j]] = 1
                else:
                    num_SHead[i[j]] += 1
                skip = False
            else:
                if pre not in num_S2S:
                    num_S2S[pre] = {i[j]: 1}
                elif i[j] not in num_S2S[pre]:
                    num_S2S[pre][i[j]] = 1
                else:
                    num_S2S[pre][i[j]] += 1
                if t != len(i) - 1:
                    pre = i[j]
                    if pre not in num_stateforS:
                        num_stateforS[pre] = 1
                    else:
                        num_stateforS[pre] += 1
    num_stc = len(data_new)
    del data_new
    gc.collect()
    for i in StatesList:
        stlist = []
        oblist = []
        AllZero = True
        if i not in num_SHead:
            OrglStateProb = np.insert(OrglStateProb, len(OrglStateProb), values=0.0, axis=0)
        else:
            OrglStateProb = np.insert(OrglStateProb, len(OrglStateProb), values=num_SHead[i] / num_stc, axis=0)
        for t, j in enumerate(StatesList):
            if t == len(StatesList) - 1:
                if AllZero == False or (i in num_S2S and j in num_S2S[i]):
                    prob = 1.0
                    for k in stlist:
                        prob -= k
                    stlist.append(prob)
                else:
                    stlist = np.ones([t + 1], np.float) * (1 / (t + 1))
                    stlist[t] = 1 - t / (t + 1)
            elif i not in num_S2S or j not in num_S2S[i]:
                stlist.append(0.0)
            else:
                stlist.append(num_S2S[i][j] / num_stateforS[i])
                AllZero = False
        TransProb.append(stlist)
        for t, j in enumerate(ObsvList):
            if j not in num_S2O[i]:
                oblist.append(0.0)
            else:
                oblist.append(num_S2O[i][j] / num_stateforO[i])
            #     oblist.append(num_S2O[i][j] / (num_stateforO[i] + 1))
            # if t == len(ObsvList) - 1:
            #     oblist.append(1 / (num_stateforO[i] + 1))
        EmissProb.append(oblist)
    del num_stateforO
    del num_stateforS
    del num_S2O
    del num_S2S
    del num_SHead
    gc.collect()
    TransProb = np.array(TransProb)
    EmissProb = np.array(EmissProb)
    # ObsvList.append("unknown")
    return StatesList, ObsvList, OrglStateProb, TransProb, EmissProb


# StatesList, ObsvList, OrglStateProb, TransProb, EmissProb = InfoExct("./data/test3.txt")
# print(StatesList)
# print(ObsvList)
# print(OrglStateProb)
# print(TransProb)
# print(EmissProb)
# print(len(StatesList))
# print(len(ObsvList))
# print(np.shape(OrglStateProb))
# print(np.shape(TransProb))
# print(np.shape(EmissProb))
