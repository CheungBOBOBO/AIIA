import multiprocessing
from bin.utils import *
from tqdm import tqdm
import numpy as np
# 导入模型
# model = gensim.models.KeyedVectors.load_word2vec_format("../etc/sgns.wiki.word",binary=False,encoding="utf8")
#
# print(model["哈哈哈哈哈哈"])


def gen_model_dict():
    words =[]
    with open("../etc/sgns.wiki.word",encoding="utf8") as fr:
        for line in tqdm(fr):
            words_temp = line.split(" ")
            words.append(words_temp[0])
    save_list(words,"../etc/embedding.dict")
# gen_model_dict()


def func():
    dict_a = load_dianli_corpus_list("../etc/embedding.dict")
    dict_b = load_dict("../result/v1/dict_split_2_filter.txt")
    # dict_b = load_dianli_corpus_list("../etc/concat.dict")
    # dict_b = load_dianli_corpus_list("../data/my_dict/sougou.txt")

    common = list(set(dict_a) & set(dict_b))
    save_list(common,"../etc/common.dict")
    print(len(common))
    print(common)

def func1():
    # dict_a = load_dianli_corpus_list("../etc/embedding.dict")
    dict_b = load_dianli_corpus_list("../etc/concat.dict")
    dict_a = load_dianli_corpus_list("../data/my_dict/sougou.txt")

    common = list(set(dict_b) - set(dict_a))
    save_list(common,"../etc/diff.dict")
    print(len(common))
    print(common)

def func2():
    dict_b = load_dict("../result/v1/dict_split_2_filter.txt")
    mm = load_dianli_corpus_list("../etc/mm.csv")
    result = []
    for word,freq in dict_b.items():
        if freq<=150:
            break
        if word in mm:
            continue
        result.append(word)
    save_list(result,"no_zhuanye.dict")
#func2()

def train():
    from gensim.models import word2vec
    sentences = word2vec.LineSentence("../data/corpus/clear_partice.txt")
    model = word2vec.Word2Vec(sentences,hs=1, min_count=1,window=3,iter=100,size=100,workers=multiprocessing.cpu_count())

    model.save("../etc/dianli_model_my.bin")

def testmodel():
    from gensim.models import word2vec
    model = word2vec.Word2Vec.load("../etc/dianli_model_my.bin")
    print(model.wv.vocab.keys())
    print(model.vector_size)
    print(model["电网"].shape)
    # for key in model.wv.similar_by_word("变压器"):
    #     print(key)
# testmodel()
sentence_vector = np.zeros(shape=(100,))
sentence_vector[1]=1
print(sentence_vector)