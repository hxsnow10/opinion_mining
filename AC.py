#encoding=utf-8
import gc

class AC_ah(object):

    def __init__(self, keys):
        import ahocorasick
        self.keys=keys
        A = ahocorasick.Automaton()
        for key in keys:
            A.add_word(key, key)
        A.make_automaton()
        self.A=A

    def get_locss(self, text):
        # if not self.keys: return []
        locss=[[key,end_idx-len(key)+1,end_idx+1] for end_idx, key in self.A.iter(text)]
        return locss

class AC_esm(object):

    def __init__(self, keys):
        import esm
        index = esm.Index()
        self.keys=keys
        for key in keys:
            index.enter(key)
        index.fix()
        self.A=index

    def get_locss(self, text):
        if not self.keys: return []
        locss=[[key,start,end] for (start,end),key in self.A.query(text)]
        return locss
AC=AC_ah

if __name__=="__main__":
    while True:
        # a=AC(["你","wo "])
        a=AC([])
        s="你妹啊。。。。%41"
        # s=""
        try:
            b=a.get_locss(s)
        except:
            pass
