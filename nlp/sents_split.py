# encoding=utf-8
import re
# from get_lang import get_lang

class SentsSplit(object):

    def __init__(self, splits, before_splits=[]):
        escape_splits=[re.escape(s) for s in splits]
        self.split=re.compile(u'('+u'|'.join(escape_splits)+u')', re.UNICODE)
        self.after_splits=set(splits)
        self.before_splits=before_splits

    def transform(self, text):
        toks=self.split.split(text.decode('utf-8'))
        toks=[tok for tok in toks if tok]
        sents=[]
        tmp=''
        k=0
        while k<len(toks):
            tok=toks[k]
            if tok in self.after_splits and\
            not (tok=='.' and k>1 and toks[k-1][-1] in u"0123456789" and k+1<len(toks) and toks[k-1][0] in u"0123456789"):
                tmp+=tok
                while k+1<len(toks) and toks[k+1] in self.after_splits:
                    k+=1
                    tmp+=toks[k]
                sents.append(tmp)
                tmp=''
            elif tok in self.before_splits:
                sents.append(tmp)
                tmp=tok
            else:
                tmp+=tok
            k+=1
        if tmp:
            sents.append(tmp)
        sents = [sent.encode('utf-8') for sent in sents]
        return sents

general_end_marks=u""".!?。！？؟\n\t】　"""
general_end_marks2=u""",，;；-()[]{}（）.!?。！？؟\n\t】　"""
hidi_end_marks=u"""!?.\n"""
thai_end_marks=u""" 　\n"""
general_sents_split=SentsSplit(general_end_marks2)
hidi_sents_split=SentsSplit(hidi_end_marks)
thai_sents_split=SentsSplit(thai_end_marks)
def sents_split(text, lang=None):
    if not lang:
        lang='zh'
        #lang=get_lang(text)
    if lang=='hi' or lang=='bn':
        sents=hidi_sents_split.transform(text)
    elif lang=='th':
        sents=thai_sents_split.transform(text)
    else:
        sents=general_sents_split.transform(text)
    return sents
