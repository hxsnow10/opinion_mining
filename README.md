Opinion Mining
===============
```
├── data                训练数据
│   ├── elm_tok.txt
│   ├── elm.txt
│   ├── elm_vec.txt
│   ├── senti_dict.txt
│   └── vocab.txt
├── result              训练结果，最终result/result.txt
│   ├── aspect2opinion.pkl
│   ├── aspect_opinion_cluster.txt
│   ├── aspects_cluster.txt
│   ├── elm_result.txt
│   ├── expand.txt
│   ├── opinions_cluster.txt
│   └── result.txt
├── cluster_aspects.py  对aspect聚类@2
├── cluster_opinion.py  对相同类aspect的opinion聚类@3
├── extract_asp_opin.py 从ekm_tok.txt提取aspect与opinion@1
├── rule_predict.py     最终的预测模型类代码@4
├── predict.py          最终的产生代码，从excel读入，并生成新的结果excel文件@5
```
@0-5 表示执行顺序。@1,@2,@3最终手动整理result.txt，可以再用vec_similar.py找一些近义词加进去。
