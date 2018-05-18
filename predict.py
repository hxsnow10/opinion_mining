# encoding=utf-8
import os
from rule_predict import DictBaseTag
# from excel_utils import read_excel, write_excel 
import csv
from os import makedirs

model=DictBaseTag("result/result.txt")
aspect_names=model.aspects.keys()
aspect2index={aspect:k for k,aspect in enumerate(aspect_names)}
todo_dir="zhengongfu2"
result_dir="zhengongfu2_result"
def clean(values):
    rval=[]
    for v in values:
        if not v:rval.append(v)
        else:
            rval.append(str(v).decode('utf-8','replace').encode('gbk','replace'))
    return rval
k=0
for dirpath, dirnames, filenames in os.walk(todo_dir):
    for filename in filenames:
        if "readMe" in filename:continue
        if "unicode" in filename:continue
        print dirpath, filename
        # makedirs(dirpath.replace(todo_dir,result_dir))
        ii=open(os.path.join(dirpath,filename),'rU')
        ii=(line.replace('\0','') for line in ii)
        i=0
        for values in csv.reader(ii):
            try:
                values=[v.strip() for v in values]
                values=[value.decode('gbk','replace').encode('utf-8','replace') for value in values]
                print len(values)
                print '/'.join(values)
                print "评价内容" in values
                if i==0:
                    if "评价内容" not in values:break
                    k=values.index("评价内容")
                    if values[-5:]==["餐品出错","配餐出错","服务态度","送餐速度","其他"]:
                        print "skip tail", filename
                        last=len(values)-5
                    else:
                        last=len(values)
                    l=len(values)
                    oo1=open(os.path.join(result_dir,filename), 'w')
                    writer1 = csv.writer(oo1,quotechar = '"')
                    oo2=open(os.path.join(result_dir,filename.replace(".csv","only_commnet.csv")), 'w')
                    writer2 = csv.writer(oo2,quotechar = '"')
                    values=values[:last]+aspect_names
                    values=clean(values)
                    writer1.writerow(values)
                    writer2.writerow(values)
                else:
                    text=values[k]
                    if not text:
                        pads=[None,]*len(aspect_names)
                    else:
                        tags=model.predict_sent(text)
                        pads=[None,]*len(aspect_names)
                        for aspect, tag in tags:
                            pads[aspect2index[aspect]]=tag
                    values=values[:last]+pads
                    print text,'/'.join([x[1] for x in tags])
                    values=clean(values)
                    writer1.writerow(values)
                    if text.strip():
                        writer2.writerow(values)
            except Exception,e:
                values=clean(values)
                writer1.writerow(values)
                print e
                pass
            i+=1
        k+=1
        

#model=DictBaseTag("result/result.txt")


