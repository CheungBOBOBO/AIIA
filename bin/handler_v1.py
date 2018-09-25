import jieba
import os
import jieba.posseg as pseg
from collections import defaultdict
from tqdm import tqdm
import re
jieba.load_userdict("../etc/sougou.txt")
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
hanzi_regex = re.compile(r'[\u4E00-\u9FA5]')
def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    global zh_pattern
    match = zh_pattern.search(word)

    return match

dianli_corpus_filepath="../data/电力语料.txt"
temp_path="../result/v1"
os.makedirs(temp_path,exist_ok=True)

def count_chinese_char_nums(sentence):
    """
    统计汉字的个数
    :param sentence
    :return:
    """
    hanzi_list = hanzi_regex.findall(sentence)
    return len(hanzi_list)

def is_luanma(sentence):
    """
    是否为乱码句子
    :return:
    """

    def new_len(iterable):
        try:
            return iterable.__len__()
        except AttributeError:
            return sum(1 for _ in iterable)

    luanma_len = len(sentence)
    luanma = jieba.cut(sentence)
    luanma_percent = luanma_len / new_len(luanma)
    if (luanma_percent<1.2):
        return True
    return False

def participle():
    # 分词
    result = defaultdict(int)
    with open(dianli_corpus_filepath,mode="r",encoding="utf8") as fr:
        for line in tqdm(fr.readlines()):
            words = pseg.cut(line)
            for word in words:
                result[word.word]+=1
        print()
    print(result)
    # 写入文件
    write_path = os.path.join(temp_path,"./dict_split.txt")
    with open(write_path,mode="w",encoding="utf8") as fw:
        for word,freq in result.items():
            fw.write("{},{}\n".format(word,freq))

def filter():
    """过滤字典，去掉一些不像专业词的词"""
    read_path = os.path.join(temp_path, "./dict_split.txt")
    result_path = os.path.join(temp_path, "./result.csv")
    filter_result = []
    with open(read_path,mode="r",encoding="utf8") as fr:
        for line in tqdm(fr.readlines()):
            if "," not in line:
                continue
            word = line.strip().split(",")[0]
            freq = line.strip().split(",")[-1]
            # 跳过单个字的词
            if len(word)<=1:
                continue
            # 跳过低频词
            if int(freq) < 50:
                continue
            # 跳过 包含英文
            if not contain_zh(word):
                continue
            # 追加到line中
            filter_result.append(word)

    # 写文件
    with open(result_path,mode="w",encoding="utf8") as fw:
        for line in filter_result:
            fw.write("{}\n".format(line))

def subtraction_commonword():
    """去掉常用词"""

def filter_dict():
    """
    过滤字典中词有没有在语料中出现
    :return:
    """
    ci_dict = "../etc/国网江西吉安电力系统常用词库整理.txt"
    yuliao=""
    with open(dianli_corpus_filepath, mode="r", encoding="utf8") as fr:
        yuliao = list(fr.readlines())
    yuliao = "\n".join(yuliao)
    print(type(yuliao))
    result=[]
    with open(ci_dict, mode="r", encoding="utf8") as fr:
        for line in tqdm(fr.readlines()):
            line = line.strip()
            if line in yuliao:
                result.append(line)
    print(len(result))
 # 写文件
    result_path = os.path.join(temp_path, "./result2.csv")
    with open(result_path,mode="w",encoding="utf8") as fw:
        for line in result:
            fw.write("{}\n".format(line))

def split_lines():
    MAX_LINE_NUMS = 100000
    with open(dianli_corpus_filepath, mode="r", encoding="utf8") as fr:
        all_line = list(fr.readlines())
        for i in range(0,len(all_line), MAX_LINE_NUMS):
            write_path = os.path.join("../data/split/", "./电力语料_{}.txt".format(i))
            with open(write_path,mode="w",encoding="utf8") as fw:
                fw.writelines(all_line[i:i+MAX_LINE_NUMS])
def main():
    #participle()
    #filter()
    #filter_dict()
    #split_lines()
    # sententce = "对于一条馈线，假设在除了变电站出线断路器以外的W处另配置一级断路器和继电保护装置，并且该继电保护装置能够与该馈线的变电站出线断路器实现部分配合，配合率为"
    # words = jieba.cut(sententce)
    # print(" ".join(words))
    #filter_lines()
    #write_fenci()
    #statict_nums()
    sort_dict()
    pass

def filter_lines():
    result_lines =[]
    with open(dianli_corpus_filepath,mode="r",encoding="utf8") as fr:
        for line in tqdm(fr.readlines()):
            if len(line) < 20:
                continue
            if count_chinese_char_nums(line)/len(line)<0.5:
                continue
            if is_luanma(line):
                continue
            result_lines.append(line)

    # 写文件
    print(len(result_lines))
    with open("../data/clear_电力语料.txt",mode="w",encoding="utf8") as fw:
        for line in result_lines:
            fw.write("{}".format(line))

def write_fenci():
    """
    把结巴分词的结果，缓存下来
    :return:
    """
    result_lines = []
    with open("../data/clear_电力语料.txt", mode="r", encoding="utf8") as fr:
            for line in tqdm(fr.readlines()):
                words = jieba.cut(line.replace(" ",""))
                sentence = " ".join(words)
                result_lines.append(sentence)
    with open("../data/clear_partice_电力语料.txt", mode="w", encoding="utf8") as fw:
        fw.writelines(result_lines)

def statict_nums():
    result = defaultdict(int)
    with open("../data/clear_partice_电力语料.txt",mode="r",encoding="utf8") as fr:
        for line in tqdm(fr.readlines()):
            words = line.split(" ")
            for word in words:
                result[word]+=1
    # 写入文件
    write_path = os.path.join(temp_path,"./dict_split_2.txt")
    with open(write_path,mode="w",encoding="utf8") as fw:
        for word,freq in result.items():
            fw.write("{},{}\n".format(word,freq))

def sort_dict():
    dict_my = {}
    with open(os.path.join(temp_path,"./dict_split_2.txt"),
              mode="r",encoding="utf8") as fr:
        for line in fr.readlines():
            if line.count(",")>1:
                print(line)
                continue
            word,freq = line.split(",")
            freq = int(freq)
            if len(word)<=2:
                continue
            if count_chinese_char_nums(word) != len(word):
                continue
            dict_my[word]=freq
    # 排序word
    write_path = os.path.join(temp_path,"./dict_split_2_filter.txt")
    with open(write_path,mode="w",encoding="utf8") as fw:
        for word,freq in sorted(dict_my.items(),key=lambda item:item[1], reverse=True):
            fw.write("{},{}\n".format(word,freq))
if __name__ == "__main__":
    main()