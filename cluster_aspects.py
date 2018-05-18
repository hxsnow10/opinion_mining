# encoding=utf-8
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from collections import defaultdict
import cPickle as pickle
from utils import dfint,cluster,w2v,output_cluster

aspect2opinion=pickle.load(open("result/aspect2opinion.pkl",'r'))
aspect2count={k:len(aspect2opinion[k].values()) for k in aspect2opinion}
print len(aspect2count)

aspect_names=[]
opinion_names=[]
opinion2count=defaultdict(int)

for aspect in aspect2opinion:
    if aspect not in w2v:continue
    aspect_names.append(aspect)
    for opinion in aspect2opinion[aspect]:
        if opinion not in w2v:continue
        opinion2count[opinion]+=1
opinion_names=opinion2count.keys()

def work(names, path, count):
    labels=cluster(names,num=25)
    names=[name+"~"+str(count[name]) for name in names]
    oo=open("result/{}_cluster.txt".format(path),'w')
    output_cluster(oo, labels, names)

work(aspect_names, "aspects", aspect2count)
work(opinion_names, "opinions", opinion2count)
