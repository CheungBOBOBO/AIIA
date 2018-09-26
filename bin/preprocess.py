from bin.utils import *
import os
from tqdm import tqdm
from collections import defaultdict
from multiprocessing import Pool

#jieba.load_userdict("../etc/sougou.txt")

class CorpusPath:
    CLEAR_PARTICIPLE_PATH="../data/corpus/clear_partice_电力语料.txt"
    CLEAR_PATH="../data/corpus/clear_电力语料.txt"

def corpus_split_lines():
    """
    将原始语料 拆分为多个小文件
    :return:
    """
    MAX_LINE_NUMS = 100000
    all_line = load_dianli_corpus_list()
    for i in range(0,len(all_line), MAX_LINE_NUMS):
        write_path = os.path.join("../data/split/", "./电力语料_{}.txt".format(i))
        with open(write_path,mode="w",encoding="utf8") as fw:
            fw.writelines(all_line[i:i+MAX_LINE_NUMS])

def corpus_filter_lines():
    """
    过滤原始语料，去掉一些无意义的句子
    :return:
    """
    result_lines =[]
    all_line = load_dianli_corpus_list()
    for line in tqdm(all_line):
        if len(line) < 20:
            continue
        if count_chinese_char_nums(line)/len(line)<0.5:
            continue
        if is_luanma(line):
            continue
        result_lines.append(line)

    # 写文件
    print(len(result_lines))
    save_list(result_lines,CorpusPath.CLEAR_PATH)
    return CorpusPath.CLEAR_PATH

def corpus_participle():
    """
    把结巴分词的结果，缓存下来
    :return:
    """
    result_lines = []
    for line in tqdm(load_dianli_corpus_list(CorpusPath.CLEAR_PATH)):
        words = jieba.cut(line.replace(" ",""))
        sentence = " ".join(words)
        result_lines.append(sentence)
    save_list(result_lines, CorpusPath.CLEAR_PARTICIPLE_PATH)

def corpus_filter_by_in(my_list):
    """
    过滤是否在在列表中
    :param my_list:
    :return:
    """
    corpus_text = load_dianli_corpus_text()
    print(len(corpus_text))
    result = []
    for word in tqdm(my_list):
        if word in corpus_text:
            result.append(word)

    # result = [word for word in tqdm(my_list) if word in corpus_text]

    return result

def corpus_word_count(corput_path=CorpusPath.CLEAR_PARTICIPLE_PATH):
    """
    统计语料分词后的词频，空格 为分隔符
    :param corput_path:
    :return:
    """
    result = defaultdict(int)
    corpus_lines = load_dianli_corpus_list(corput_path)
    for line in tqdm(corpus_lines):
        words = line.split(" ")
        for word in words:
            result[word] += 1
    return result
