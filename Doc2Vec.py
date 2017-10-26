import time
from gensim.models import Word2Vec
import pickle
import numpy as np
import pandas as pd
# from Labeled.preProcess import createCSV

# timer2 = time.time()
# model = Word2Vec.load("./300Features_HamShahri.bin")
# timer3 = time.time()
# print("model loaded in %d seconds", timer3 - timer2)


def AvgSent2vec(words, model):
    # words = str(s).lower()  # .decode('utf-8')
    # words = word_tokenize(words)
    # words = [w for w in words if not w in stop_words]
    # words = [w for w in words if w.isalpha()]
    M = []
    for w in words:
        try:
            # print(w)
            M.append(model[w])
        except:
            # print("there isn't")
            continue
    M = np.array(M)
    v = M.mean(axis=0)
    return v / np.sqrt((v ** 2).sum())


def represent(data, word, model):
    data = data.dropna()
    print(data.shape)
    print(data.head())
    q1FVecs = np.zeros((data.shape[0], 300))

    for index, row in data.iterrows():
        q1FVecs[index] = AvgSent2vec(row[0].split(" "),model)
    print("features calculated")
    train_df = pd.DataFrame(q1FVecs)

    train_df.to_csv(str(word) + 'contexts' + 'AvgSent2vec.csv', index=False)
    return train_df


# word = 'اشکال'
# represent(pd.read_csv(str(word) + 'contexts.csv'), word)
