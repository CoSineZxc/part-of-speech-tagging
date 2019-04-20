from hmmlearn import hmm
import numpy as np
import pickle
from fileop import InfoExct

# HMM五元组
StatesList, ObsvList, OrglStateProb, TransProb, EmissProb = InfoExct("./data/test.txt")
num_state=len(StatesList)
model=hmm.MultinomialHMM(n_components=num_state)
model.startprob_=OrglStateProb
model.transmat_=TransProb
model.emissionprob_=EmissProb

fw=open('model/model3.txt', 'wb')
pickle.dump(model, fw)
pickle.dump(ObsvList,fw)
pickle.dump(StatesList,fw)
fw.close()
print('** Finished saving the data.')