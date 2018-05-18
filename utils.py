# encoding=utf-8
from nlp.word2vec import load_w2v
from sklearn.cluster import KMeans, DBSCAN
from collections import defaultdict
def dfint():
    return defaultdict(int)

def load_senti_dict(senti_dict_path="data/senti_dict.txt"):
    ii=open(senti_dict_path,'r')
    senti_dict={}
    for line in ii:
        word, p =line.strip().split()
        if p!='1' and p!='-1':continue
        senti_dict[word]=p 
    return senti_dict

senti_dict=load_senti_dict()

w2v=load_w2v("data/elm_vec.txt", norm=True)
def cluster(names, num):
    X=[w2v.get(name,w2v['</s>']) for name in names]
    if not X:return []
    cl = KMeans(n_clusters=num, random_state=0, n_jobs=10)
    cl.fit(X)
    return cl.labels_

def output_cluster(oo, labels, names):
    ids=set(labels)
    
    for i in ids:
        oo.write(str(i)+':')
        nn=[]
        for k,j in enumerate(labels):
            if j==i:
                nn.append(names[k])
        #nn=sorted(nn,key=lambda x:int(x.split('~')[-1]), reverse=True)
        oo.write('/'.join(nn)+'\n')
        #oo.write('/'.join([x.split('~')[0] for x in nn])+'\n')
