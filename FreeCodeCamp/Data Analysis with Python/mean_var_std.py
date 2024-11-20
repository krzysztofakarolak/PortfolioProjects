# Project number 1
import numpy as np

def calculate(list):
    if len(list)!=9:
      raise ValueError("List must contain nine numbers.")
    else:
      list=np.array(list)
      y=list.reshape(3,3)
      calculations={'mean': [np.mean(y,axis=0).tolist(), np.mean(y,axis=1).tolist(), np.mean(y).tolist()],
             'variance': [np.var(y,axis=0).tolist(), np.var(y,axis=1).tolist(), np.var(y).tolist()],
             'standard deviation': [np.std(y,axis=0).tolist(), np.std(y,axis=1).tolist(), np.std(y).tolist()],
             'max': [np.max(y,axis=0).tolist(), np.max(y,axis=1).tolist(), np.max(y).tolist()],
             'min': [np.min(y,axis=0).tolist(), np.min(y,axis=1).tolist(), np.min(y).tolist()],
             'sum': [np.sum(y,axis=0).tolist(), np.sum(y,axis=1).tolist(), np.sum(y).tolist()]}
    return calculations