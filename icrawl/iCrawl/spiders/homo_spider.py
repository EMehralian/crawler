import scrapy
import re
import pandas as pd
import os.path




class homographSpider(scrapy.Spider):
    name = "homograph"
    size = 0

    def start_requests(self):
        word = 'مفصل'
        urls = ['https://fa.wikipedia.org/w/index.php?search=مفصل&title=ویژه:جستجو&profile=advanced&fulltext=1&ns2=1&searchToken=83etzo3c1e150zj9t9ctzuzhnhttps://fa.wikipedia.org/w/index.php?search=مفصل&title=ویژه:جستجو&profile=advanced&fulltext=1&ns2=1&searchToken=83etzo3c1e150zj9t9ctzuzhn']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def striphtml(self, data):
        return re.sub('<[^>]*>', '', data)

    def containsH(self, sentence):
        with open('homogenous.csv') as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        words = sentence.split(' ')
        for word in words:
            if content.__contains__(word):
                return sentence
        return False

    def parse(self, response):
        page = response.xpath('//*[@id="mw-content-text"]/div/ul/li[1]//*[@id="mw-content-text"]/div/ul/li[1]').extract()
        for paraghraph in page:
            sentences = self.striphtml(paraghraph).split('.')

            for sentence in sentences:
                sentence = sentence.replace('\n', '')
                sentence = re.sub(r"\[([۰-۹_]+)\]", '', sentence)

                if self.containsH(sentence):
                    self.size += 1
                    # print(sentence)
                    yield {
                        'sentence': sentence
                    }

        pageLinks = response.css('a::attr(href)').extract()

        if pageLinks is not None:
            for link in pageLinks:
                # if os.path.isfile('./../../ehsan.csv'):
                #     train = pd.read_csv('./../../ehsan.csv')
                #     shape = train.shape
                #     if shape[0] < 1000:
                if self.size < 1000:
                    if link.startswith("/wiki"):
                        next_page = response.urljoin(link)
                        # yield next_page
                        yield scrapy.Request(next_page, callback=self.parse)
