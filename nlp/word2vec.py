#encoding=utf-8
import gensim
import numpy as np    
from collections import OrderedDict

class gensim_model():
    
    def __init__(self, model_path):
        model = gensim.models.Word2Vec.load_word2vec_format(model_path, binary=False)

    def most_similar(self, word):
        pass

def normalized(a, axis=-1, order=2):
    """Utility function to normalize the rows of a numpy array."""
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1 
    return a / np.expand_dims(l2, axis)

def load_w2v(w2v_path, dtype=np.float16, norm=False, max_vocab_size=None, limited_words=[]):
    limited_words=set(limited_words)
    ii=open(w2v_path,'r')
    n,l=None,None
    try:
        n,l=ii.readline().strip().split()
        n,l=int(n),int(l)
    except:
        pass
    w2v=OrderedDict()
    w2v.dim=l
    for k,line in enumerate(ii):
        try: 
            wl=line.strip().split()
            word=wl[0]
            if limited_words and word not in limited_words:continue
            value=[float(x) for x in wl[1:]]
            assert len(value)==l or not l
            value=np.array(value, dtype=dtype)
            if norm:
                value=normalized(value)[0]
            w2v[word]=value
        except:
            print line
        if max_vocab_size and k>=max_vocab_size:break

    return w2v

def save_w2v(w2v, w2v_path):
    oo=open(w2v_path,'w')
    l=0
    for x in w2v:
        l=w2v[x].shape[0]
        break
    n=len(w2v)
    oo.write(str(n)+' '+str(l)+'\n')
    for w,v in w2v.iteritems():
        oo.write(' '.join([w]+[str(x) for x in list(v)])+'\n')
    
