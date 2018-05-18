# encoding=utf-8
from collections import defaultdict
from AC import AC
from jieba import Tokenizer
from nlp.sents_split import sents_split
from gensim.models import word2vec
mm=Tokenizer("dict.txt")
import json
def zh_tok(sent):
    return [x.encode('utf-8') for x in mm.cut(sent)]

def jprint(x, s=None):
    return
    if s:print s
    try:
        print json.dumps(x, ensure_ascii=False)
    except:
        print x

antis=["不","没有","一点也不","没","未"]
class DictBaseTag(object):

    def __init__(self, dict_path):
        self.read_dict(dict_path)

    def read_dict(self, dict_path):
        ii=open(dict_path, 'r')
        aspect_id=None
        self.aspects={}
        self.word2aspect=defaultdict(list)
        self.word2opinion=defaultdict(list)
        self.opinions={}
        for line in ii:
            try:
                line=line.strip()
                if not line:
                    aspect_id=None
                elif line.startswith("aspects"):
                    _,aspect_name,words=line.split("=")
                    aspect_id=aspect_name
                    words=[x for x in words.split("/") if x]
                    self.aspects[aspect_name]=words
                    for word in words:
                        self.word2aspect[word].append(aspect_name)
                else:
                    opinion_phrase,words=line.split("=")
                    opinion_phrase,anti_opinion_phrase=opinion_phrase.split("/")
                    words1,words2=words.split("$")
                    words1=[x for x in words1.split("/") if x]
                    words2=[x for x in words2.split("/") if x]
                    a=self.opinions[opinion_phrase]=type('MyObject', (object,), {})
                    a.aspect_id=aspect_id
                    a.words1=words1
                    a.words2=words2
                    a.opinion_phrase=opinion_phrase
                    a.anti_opinion_phrase=anti_opinion_phrase

                    for word in words1+words2:
                        self.word2opinion[word].append(opinion_phrase)
            except Exception,e:
                print e
                print line
        self.AC=AC(list(set(self.word2aspect.keys()+self.word2opinion.keys())))
    
    def predict_sent(self, sent):
        rval=[]
        phrases=sents_split(sent)
        for phrase in phrases:
            tags=self.predict_phrase(sent)
            rval=rval+tags
        return list(set(rval))

    def predict_phrase(self, sent):
        words=self.search_words(sent)
        aspect_ids=sum([self.word2aspect[word] for loc,word in words], [])
        opinion_phrases=sum([self.word2opinion[word] for loc,word in words], [])
        jprint(words)
        jprint(aspect_ids)
        jprint(opinion_phrases)
        result=[]
        for loc,word in words:
            anti=self.find_anti(sent,loc)
            for opinion_phrase in self.word2opinion[word]:
                print anti,loc,word,opinion_phrase
                jprint(opinion_phrase)
                opinion=self.opinions[opinion_phrase]
                if word in opinion.words2 or (opinion.aspect_id and opinion.aspect_id in aspect_ids):
                    if anti:
                        result.append((opinion.aspect_id,opinion.anti_opinion_phrase))
                    else:
                        result.append((opinion.aspect_id,opinion.opinion_phrase))
        return result

    def search_words(self, sent):
        words=zh_tok(sent)
        jprint(words)
        word_starts,reverse_word_starts=[0],{0:0}
        for k,word in enumerate(words):
            l=word_starts[-1]+len(word)
            word_starts.append(l)
            reverse_word_starts[l]=k+1
        word_starts.append(len(sent))
        original_sent=''.join(words)
        word_starts=set(word_starts)
        locss = self.AC.get_locss(original_sent)
        jprint(word_starts, "word_starts")
        jprint(locss,"before_filer")
        # locss = [[(start,end),sent[start:end]] for key,start,end in locss ]
        locss = [[(start,end),sent[start:end]] for key,start,end in locss if start in word_starts and end in word_starts]
        jprint(locss,"after_filer")
        return locss

    def find_anti(self, sent, loc):
        print loc
        s,e=loc
        sub=sent[0:s]
        print sub
        words=zh_tok(sub)
        print json.dumps(words, ensure_ascii=False)
        for word in words[-4:]:
            if word in antis:
                return True
        return False

    def expand(self):
        old_words=set(self.word2aspect.keys()+self.word2opinion.keys())
        model=word2vec.Word2Vec.load_word2vec_format("data/elm_vec.txt",binary=False)
        
        def expand_words(words, th=0.55):
            rval=defaultdict(float)
            for w in words:
                try:
                    similar=model.most_similar(w.decode('utf-8'), topn=60)
                    for ww,p in similar:
                        if p>=th:
                            if ww.encode('utf-8') in old_words:continue
                            rval[ww.encode('utf-8')]+=p
                except:
                    pass
            rval=sorted(rval.iteritems(), key=lambda x:x[1], reverse=True)
            rval=[x[0] for x in rval]
            return rval
        
        oo=open("result/expand.txt",'w')
        for aspect_name in self.aspects:
            words = self.aspects[aspect_name]
            oo.write("aspect{} new_words".format(aspect_name)+'\t'+'/'.join(words)+'\n'+'/'.join(expand_words(words))+'\n')
            for opinion_phrase in self.opinions:
                a=self.opinions[opinion_phrase]
                if a.aspect_id==aspect_name:
                    words=a.words1+a.words2
                    oo.write("aspect{} opinion{} new_words".format(aspect_name, opinion_phrase)+'\t'+'/'.join(words)+'\n'+'/'.join(expand_words(words))+'\n')

if __name__=="__main__":
    model=DictBaseTag("result/result.txt")
    import json
    print json.dumps(model.predict_phrase("麦香鱼有异味。"), ensure_ascii=False)
    quit()
    model.expand()
    ii=open("data/elm.txt",'r')
    oo=open("result/elm_result.txt",'w')
    for line in ii:
        tags=model.predict_sent(line)
        if tags:
            oo.write(line)
            oo.write('\t'+'\t'.join(tags)+'\n')

