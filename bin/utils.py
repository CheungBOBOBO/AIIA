import re
import jieba

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
dianli_corpus_filepath="../data/corpus/电力语料.txt"

def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''
    global zh_pattern
    match = zh_pattern.search(word)

    return match

def count_chinese_char_nums(sentence):
    """
    统计汉字的个数
    :param sentence
    :return:
    """
    hanzi_list = zh_pattern.findall(sentence)
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

def filter_dict(dict_in):
    """
    过滤字典，把字典中的明显不是的词不考虑
    :param dict_in:
    :return:
    """
    dict_result = {}
    for word,freq in dict_in:
        # 跳过单个字的词
        if len(word) <= 1:
            continue
        # 跳过低频词
        if int(freq) < 50:
            continue
        # 跳过 包含英文
        if not contain_zh(word):
            continue
        dict_result[word] = freq
    return dict_result

def strip_freq(dict_my):
    """
    去掉字典的词频，按照词频大小返回
    :param dict_my:
    :return:
    """
    result_list = [word for word, freq in sorted(dict_my.items(), key=lambda item: item[1], reverse=True)]
    return result_list

def save_dict(dict_my,file_path):
    """
    保存字典，按照词频排序
    :param dict_my:
    :param file_path:
    :return:
    """
    with open(file_path,mode="w",encoding="utf8") as fw:
        for word,freq in sorted(dict_my.items(),key=lambda item:item[1], reverse=True):
            fw.write("{},{}\n".format(word,freq))

def save_list(list_my, file_path):
    """
    保存列表
    :param list_my:
    :return:
    """
    with open(file_path, mode="w", encoding="utf8") as fw:
        for line in list_my:
            fw.write("{}\n".format(line))

def load_dict(file_path):
    dict_out = {}
    with open(file_path, mode="r", encoding="utf8") as fr:
        for line in fr:
            try:
                if line.count(",") != 1 :
                    continue
                word = line.strip().split(",")[0]
                freq = line.strip().split(",")[-1]
                dict_out[word] = int(freq)
            except Exception as e:
                pass
    return dict_out

def load_dianli_corpus_text(my_path = dianli_corpus_filepath):
    """
    加载电力语料，原始文件
    :return: 一个字符串
    """
    result = ""
    with open(my_path,mode="r",encoding="utf8") as fr:
        result = " ".join(list(fr.readlines()))
    return result

def load_dianli_corpus_list(my_path = dianli_corpus_filepath):
    """
    加载电力语料，原始文件，返回列表
    :return:
    """
    result = []
    with open(my_path,mode="r",encoding="utf8") as fr:
        result = [line.strip() for line in fr]
    return result