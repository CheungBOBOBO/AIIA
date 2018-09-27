import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
# from gensim.models import word2vec
from tqdm import tqdm
from bin.utils import *
# 加载词向量
# model = word2vec.Word2Vec.load("../etc/dianli_model_my.bin")

def caluc_unkown_word_vector():
    """
    计算未知词的向量值
    :return:
    """
    list_key = model.wv.vocab.keys()
    count_all=len(list_key)
    unkown_word_vector = np.zeros(shape=(model.vector_size,))
    for word in list_key:
        temp_vector = model[word]
        unkown_word_vector+=temp_vector
    unkown_word_vector /= count_all

    return unkown_word_vector

# padding_word = np.zeros(shape=(model.vector_size,))
# unkown_word = caluc_unkown_word_vector()
# mm_dict = load_dict("../etc/mm.csv")
def word_to_vector(word):
    """
    把单词变成词向量,处理未知词
    :param word:
    :return:
    """
    word_vector = unkown_word
    if word in model.wv.vocab:
        word_vector = model[word]
    return word_vector

def sentence_to_vecotr(sentence,max_count=100):
    """
    讲一个句子转变为向量，转换最大的词数量
    :param sentence:
    :param max_count:
    :return:
    """
    words = str(sentence).split(" ")
    sentence_vector=None
    for index,word in enumerate(words):
        if index>=max_count:
            break
        vector_word =word_to_vector(word)
        if sentence_vector is None:
            sentence_vector = vector_word
        else:
            sentence_vector = np.append(sentence_vector,vector_word)
    for i in range(len(words),100,1):
        sentence_vector = np.append(sentence_vector,padding_word)
    return sentence_vector

def sentence_to_label(sentence,max_count=100):
    """
    标注句子里的哪个词是“专业词汇”
    :param sentence:
    :param max_count:
    :return:
    """
    sentence_vector = np.zeros(shape=(max_count,))
    words = str(sentence).split(" ")
    for i,word in enumerate(words):
        if i>=max_count:
            break
        last_word = words[i-1]
        if word in mm_dict:
            sentence_vector[i] = 1
        if i > 0 and  "{}{}".format(last_word,word) in mm_dict:
            sentence_vector[i] = 1
            sentence_vector[i - 1] = 1
    return sentence_vector

# 1.准备训练数据
def transformer_X():
    """
    准备训练数据，讲句子转变为向量
    :return:
    """
    with open("../result/v3/trainX.txt", encoding="utf8", mode="w") as fw:
        with open("../data/corpus/clear_partice.txt",encoding="utf8") as fr:
            for line in tqdm(fr.readlines()):
                sen_vector = sentence_to_vecotr(line.strip())
                line = ""
                for row in sen_vector:
                    line += str(row)
                    line += ","
                line = line[:-1]
                fw.write(line + "\n")
def transformer_Y():
    """
    准备训练数据，Y标签
    """
    with open("../result/v3/trainY.txt", encoding="utf8", mode="w") as fw:
        with open("../data/corpus/clear_partice.txt",encoding="utf8") as fr:
            for line in tqdm(fr.readlines()):
                sen_label = sentence_to_label(line.strip())
                line = ""
                for row in sen_label:
                    line += str(row)
                    line += ","
                line = line[:-1]
                fw.write(line + "\n")

def train():
    """
    训练
    :return:
    """
    print("begin training")
    # 构建模型
    print("begin model init")
    model = keras.Sequential()
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(100, return_sequences=True),
                                         input_shape=(100,100)))
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(10)))
    model.add(keras.layers.Dense(100,activation="sigmoid"))
    model.compile(loss="mean_squared_error", optimizer="adam")
    # 加载数据
    print("data init")
    trainx = pd.read_csv("../result/v3/trainX.txt",encoding="utf8",header=None)
    trainy = pd.read_csv("../result/v3/trainY.txt",encoding="utf8",header=None)
    trainx = trainx.values.reshape((trainx.values.shape[0],100,100))
    trainy = trainy.values.reshape((trainy.values.shape[0], 100))
    # 训练
    print("fit")
    model.fit(trainx, trainy, epochs=400, batch_size=4096, verbose=2)

    model.save("../result/v3/model.bin")

def predict():
    model = keras.models.load_model("../result/v3/model.bin")

    testx = pd.read_csv("../result/v3/trainX.txt",encoding="utf8",header=None, nrows=10)
    testx = testx.values.reshape((10,100,100))

    testy_predict = model.predict(testx)
    return testy_predict
    print(testy_predict)

def pickup_words(array,words,threld=0.9):
    """
    挑选出单词
    :param array:
    :param words:
    :param threld:
    :return:
    """
    words_return = []
    for i, prob in enumerate(array):
        if prob>threld:
            if i> len(words):
                words_return.append("<Padding>")
            else:
                words_return.append(words[i])
    return words_return

def test():
    trainy = pd.read_csv("../result/v3/trainY.txt", encoding="utf8", header=None, nrows=10)
    trainy = trainy.values.reshape((10,100))
    words = load_dianli_corpus_list("../data/corpus/clear_partice.txt")
    words = words[:10]
    words = [line.strip().split(" ") for line in words]
    testy_predict = predict()
    for i,array in enumerate(trainy):
        res = pickup_words(array,words[i])
        res_p = pickup_words(testy_predict[i], words[i])
        print("{}{}{}".format(i,res,res_p))
train()
test()

    #

