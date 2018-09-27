from gensim.models import word2vec
from bin.utils import *
from tqdm import tqdm

def handle_v2():
    result=[]
    mm_dict = load_dict("../etc/mm.csv")
    model = word2vec.Word2Vec.load("../etc/dianli_model_my.bin")
    for word,freq in tqdm(mm_dict.items()):
        result.append(word)
        if word not in model.wv.vocab:
            continue
        for sim_word,score in model.wv.similar_by_word(word, topn=100):
            if score > 0.6:
                result.append(sim_word)
    save_list(result,"../result/v1/sim.word")
handle_v2()
