# encoding=utf-8
from utils import senti_dict, dfint, cluster, output_cluster 
import cPickle as pickle
from collections import defaultdict
aspect2opinion=pickle.load(open("result/aspect2opinion.pkl",'r'))

def dict_sum(ds):
    rval=defaultdict(int)
    for d in ds:
        for key in d:
            rval[key]+=d[key]
    return rval

aspects_cluster2names=defaultdict(dfint)
aspects_cluster2opinions=defaultdict(dfint)

ii=open("result/aspects_cluster.txt",'r')
oo=open("result/aspect_opinion_cluster.txt",'w')
for line in ii:
    oo.write(line)
    parts=line.strip().split(':')
    cluster_name=parts[0]
    aspects_names=[asp.split('~')[0] for asp in ':'.join(parts[1:]).split('/')]
    print cluster_name
    print '/'.join(aspects_names)
    opinions=dict_sum([aspect2opinion[asp.split('~')[0]] for asp in aspects_names\
            if asp in aspect2opinion])
    #aspects_cluster2names[cluster_name]=aspects_names
    #aspects_cluster2opinions[cluster_name]=opinions
    print len(opinions)
    good_opinions={key:opinions[key] for key in opinions if key in senti_dict and senti_dict[key]=='1'}
    labels=cluster(good_opinions.keys(),5)
    oo.write("good_opinions:\n")
    output_cluster(oo, labels, good_opinions.keys())
    bad_opinions={key:opinions[key] for key in opinions if key in senti_dict and senti_dict[key]=='-1'}
    labels=cluster(bad_opinions.keys(),5)
    oo.write("bad_opinions:\n")
    output_cluster(oo, labels, bad_opinions.keys())

