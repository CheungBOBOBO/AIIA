import os
from collections import defaultdict
from tqdm import tqdm
from bin.utils import *
from bin.preprocess import *

temp_path="../result/v2"
os.makedirs(temp_path,exist_ok=True)

def func1():
    """
    清理 下载的各种字典，挑选出在语料中出现的词
    :return:
    """
    # 1.获得所有字典路径
    dicts_path=[os.path.join(root,file) for root,dir,files in os.walk("../data/my_dict")
                                        for file in files]
    # 2.加载字典名
    dict_result=[]
    for dict_path in dicts_path:
        dict_tmp = load_dianli_corpus_list(my_path=dict_path)
        dict_result.extend(dict_tmp)
    dict_result=list(set(dict_result))
    print("before filter ,nums = {}".format(len(dict_result)))

    # 4.筛选 字词
    dict_filer = corpus_filter_by_in(dict_result)
    print("after filter ,nums = {}".format(len(dict_filer)))

    # 5.保存 字典
    save_list(dict_filer, "../etc/my.dict")

def func2():
    """
    清理语料库，去掉乱码的句子，语料分词，统计词频
    :return:
    """
    jieba.load_userdict("../etc/my.dict")
    # 1.清理语料库
    corpus_filter_lines()

    # 2.语料分词
    corpus_participle()

    # 3.统计词频
    word_count = corpus_word_count()
    save_dict(word_count, os.path.join(temp_path,"words_count.csv"))

def main():
    func1()
    pass


if __name__ == "__main__":
    main()