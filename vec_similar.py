import numpy
from copy import deepcopy
from numpy import ndarray
import time
from multiprocessing import Pool
import sys
from gensim.models import word2vec

model=word2vec.Word2Vec.load_word2vec_format(sys.argv[1],binary=False)
while True:
    try:
        w=raw_input('Enter word:').decode('utf-8')
        if w not in model:
            print 'word not in model'
            continue
        n=raw_input('Enter n:(default 20)')
        if n.strip()=='':n=20
        else:n=int(n.strip())
        similar=model.most_similar(w, topn=n)
        for ww,p in similar:
            print ww,p
    except Exception,e:
        print 'error',e
        break
