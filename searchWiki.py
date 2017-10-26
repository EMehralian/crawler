import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import wikipedia
import pandas as pd
import re

wikipedia.set_lang("fa")

url = 'https://fa.wikipedia.org/w/index.php'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 '
                         'Safari/537.17'}


def preprocess(rawText):
    # after_word = "== منابع =="
    # cleaned_text = rawText[:rawText.index(after_word)]
    cleaned_text = re.sub("=.*?=", '', rawText, flags=re.DOTALL)
    cleaned_text = cleaned_text.replace('\n\n', '\n')
    cleaned_text = cleaned_text.replace('     ', ' ')
    cleaned_text = cleaned_text.replace('\n\n', '\n')
    return cleaned_text


def getValues(topic, limit, offset):
    return {'search': topic,
            'title': 'ویژه:جستجو',
            'profile': 'default',
            'fulltext': '1',
            'limit': limit,
            'offset': offset
            }


def search(topic, limit, offset, flag):
    values = getValues(topic, limit, offset)
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')  # data should be bytes
    dic = {}
    try:
        req = urllib.request.Request(url, data, headers=headers)
        resp = urllib.request.urlopen(req)
        html = resp.read().decode('utf8')
        parsed_html = BeautifulSoup(html, "lxml")
        nextLink = (parsed_html.body.find('a', attrs={'class': 'mw-nextlink'}))
        if flag:
            resultsNum = (
            parsed_html.body.find('div', attrs={'class': 'results-info'}).get('data-mw-num-results-total'))
            return int(resultsNum)

        print(nextLink.text)
        linksList = []
        links = (parsed_html.body.find('ul', attrs={'class': 'mw-search-results'}))
        for link in links.findAll('a'):
            try:
                dic[link.text] = preprocess(wikipedia.page(link.text).content)
            except Exception as e:
                print(e)
                # linksList.append(link.get('href'))
                # print(link.get('href'))
                # print(link.text)
        saveFile = open('links.csv', 'w')
        saveFile.write(str(linksList))
        saveFile.close()
    except Exception as e:
        print(str(e))

    pd.DataFrame.from_dict(data=dic, orient='index').to_csv(str(topic) + '.csv', header=None, mode='a')


def start(word):
    resultsNum = search(word, '10', '0', True)

    for i in range(20):
        if resultsNum > 200:
            # str(int(resultsNum / 40))
            search(word, '20', (i * (resultsNum / 20)), False)
        else:
            print("no enough pages")

    return pd.read_csv(str(word) + '.csv')

