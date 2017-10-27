from wiki.searchWiki import start
from wiki.wikiContexts import collectContext
from wiki.Doc2Vec import represent
from gensim.models import Word2Vec


def generateTestData(word, model):
    rawContexts = collectContext(word, start(word))
    return represent(rawContexts, word, model)


model = Word2Vec.load("300Features_HamShahri.bin")
print("model loaded in %d seconds")
word = 'مرکب'
generateTestData(word, model)
