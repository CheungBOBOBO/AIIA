import gensim

# 导入模型
model = gensim.models.KeyedVectors.load_word2vec_format("../etc/sgns.wiki.word",binary=False,encoding="utf8")

print(model["哈哈哈哈哈哈"])