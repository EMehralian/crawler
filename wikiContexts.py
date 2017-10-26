import pandas as pd
import pickle
import numpy as np

# homograph = pd.read_csv('Data/homograph.csv')


# print(homograph['لغت'])


# def load_obj(name):
#     with open(name + '.pkl', 'rb') as f:
#         return pickle.load(f)
#
#
# dictionary = load_obj('Data/finalTrainDictionary')
#

def load_data(name):
    data = pd.read_csv(str(name) + '.csv')
    return data


def tokenize(text):
    tokens = text.split()
    return list(tokens)


def setContext(myList, indices):
    contexts = []
    for index in indices:
        if 0 < index - 20:
            if index + 20 < len(myList):
                contexts.append(" ".join(myList[index - 20: index + 20]))
                # return " ".join(myList[index-20: index+20])
            else:
                contexts.append(" ".join(myList[index - 20:]))
                # return " ".join(myList[index - 20:])
        else:
            if index + 20 < len(myList):
                contexts.append(" ".join(myList[: index + 20]))
                # return " ".join(myList[: index + 20])
            else:
                contexts.append(" ".join(myList[:]))
                # return " ".join(myList[:])
    return contexts


def collectContext(word,data):
    extracted_contexts = []
    # data = load_data(word)
    print(data.shape)
    for index, row in data.iterrows():
        myList = tokenize(row[data.columns[1]])
        if word in myList:
            indices = [i for i, x in enumerate(myList) if x == word]
            extracted_contexts.extend(setContext(myList, indices))
    newTrain = np.asarray(extracted_contexts)
    trindex = [i for i in range(0, len(extracted_contexts))]
    train = pd.DataFrame(data=newTrain, index=trindex)
    train.to_csv(str(word) + 'contexts.csv', index=False)
    print(str(train.shape[0]) + "contexts collected")
    return train

# collectContext('اشکال')