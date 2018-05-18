# encoding=utf-8
from collections import defaultdict
from nlp.word2vec import load_w2v
import numpy as np
from collections import defaultdict
# from nlp.ltp import postagger
from nlp.sents_split import sents_split
import cPickle as pickle
from utils import senti_dict, dfint
import jieba
import jieba.posseg as pseg
def postagger(sent):
    z=[x for x in pseg.cut(sent)]
    a=[x.word.encode('utf-8') for x in z]
    b=[x.flag for x in z]
    return a,b

'''
ii=open("vocab.txt",'r')
for line in ii:
    word, count = line.strip().split()
    if word in senti_dict:
        oo.write(senti_dict[word]+'\t'+line.strip()+'\n')
'''

ii=open("data/elm_tok.txt",'r')
aspects=defaultdict(dfint)
window=5
cc=0
for line in ii:
    cc+=1
    for sent in sents_split(line,'zh'):
        toks,tags = list(postagger(sent))
        for k,tok in enumerate(toks):
            if tok in senti_dict:
                for kk in range(k-window,k+window):
                    if kk<0 or kk>=len(toks):continue
                    if kk==k:continue
                    if toks[kk] in senti_dict:continue
                    if tags[kk][0]!='n':continue
                    print toks[kk], toks[k]
                    aspects[toks[kk]][toks[k]]+=1
print len(aspects)
pickle.dump(aspects,open("result/aspect2opinion.pkl",'w'))
#'''
aspects=[[k,aspects[k],sum(aspects[k].values())] for k in aspects]
aspects=sorted(aspects, key=lambda x:x[2], reverse=True)
oo=open("aspects-opinion.txt",'w')
for aspect,info,_ in aspects:
    oo.write(aspect+":")
    info=sorted(info.iteritems(), key=lambda x:x[1], reverse=True)
    for opinion,count in info[:20]:
        oo.write(opinion+'~'+str(count)+'/')
    oo.write('\n')
#'''
