import datetime
from typing import Optional, Any, List

import requests
from bs4 import BeautifulSoup
from dateutil.tz import tzutc
from django.db import transaction

from app.models import ScrapeResult, Symbol


class Article:
    def __init__(self, link, date, title, symbol, article):
        self.link = link
        dt = datetime.datetime.strptime(date.replace(',', ''), '%m/%d/%Y %H:%M %p')
        self.posted_at = datetime.datetime.combine(dt.date(), dt.time(), tzinfo=tzutc())
        self.headline = title
        self.symbol = symbol
        self.article = article


class Service:
    @classmethod
    def execute(cls, **args):
        instance = cls(**args)
        with transaction.atomic():
            instance.process()
        return instance

    def process(self):
        raise NotImplementedError()


class AcquireScrapeResults(Service):
    def __init__(self, scrape_request):
        self.scrape_request = scrape_request
        self.scrape_results = []

    def process(self):
        self.scrape_results = self.find_list_of_nn_articles()

    # function to scrape homepage, return INDEX of articles that are 'notable/ noteworthy'
    def find_nn(self, headlines):
        note = []
        for x in range(len(headlines)):
            if 'Option Activity' in headlines[x].get_text():
                note.append(x)

        return note

    # extracts text from article html page, gathers symbols
    def extractArticle(self, link):
        aPage = requests.get(link)
        aPageContent = BeautifulSoup(aPage.content, 'html.parser')
        aPageContent.prettify()
        articleText = aPageContent.find(id='articleText')
        return articleText.get_text()

    # extracts symbols from article text
    def extractSymbols(self, article):
        s = 0
        indexes = []
        symbols = []

        for x in range(3):
            indexes.append(article.find("Symbol: ", s))
            s = article.find("Symbol: ", s) + 5

        for c in range(3):
            if article[indexes[c] + 9] == ')':
                symbols.append(article[indexes[c] + 8])
            if article[indexes[c] + 10] == ')':
                symbols.append(article[indexes[c] + 8] + article[indexes[c] + 9])
            if article[indexes[c] + 11] == ')':
                symbols.append(article[indexes[c] + 8] + article[indexes[c] + 9] + article[indexes[c] + 10])
            if article[indexes[c] + 12] == ')':
                symbols.append(
                    article[indexes[c] + 8] + article[indexes[c] + 9] + article[indexes[c] + 10] + article[
                        indexes[c] + 11])
            if article[indexes[c] + 13] == ')':
                symbols.append(article[indexes[c] + 8] + article[indexes[c] + 9] + article[indexes[c] + 10] + article[
                    indexes[c] + 11] + article[indexes[c] + 12])
        articles = article.split('highlighted in orange')
        return list(zip(symbols[0:], articles[0:len(symbols)]))

    # fins list of articles that mention 'noteworthy' or 'notable'
    def find_list_of_nn_articles(self):
        # OPENING HOMEPAGE NASDAQ.COM/OPTIONS

        page = requests.get("https://www.nasdaq.com/options")  # Opens page

        homepageContent = BeautifulSoup(page.content, 'html.parser')  # Parses html

        articleList: Optional[Any] = homepageContent.find(
            id="latest-news-headlines")  # Everything inside of <div id="latest-news-headlines">

        headlines = articleList.find_all('b')  # List: All article headlines

        noteworthyArticleIDs = self.find_nn(headlines)  # List: INDEX (int) of noteworthy articles from homepage

        articles = articleList.find_all('li')  # List: all article items on home page

        noteworthyArticleItems = []  # empty, will hold article items that are noteworthy/ notable

        finalListofArticleObjects: List[Article] = []  # the final list of Article instances to be exported

        #################################################################################################

        for x in range(len(noteworthyArticleIDs)):
            noteworthyArticleItems.append(
                articles[noteworthyArticleIDs[x]])  # adding noteworthy articles to array based on index from find_nn

        for k in range(len(noteworthyArticleItems)):
            hl = noteworthyArticleItems[k].find('b').get_text()  # Headline
            l = noteworthyArticleItems[k].find('a').get('href')  # Link
            d = noteworthyArticleItems[k].find('span').get_text()  # Date
            a = self.extractArticle(noteworthyArticleItems[k].find('a').get('href'))  # Article text
            symbols = self.extractSymbols(a)
            for symbol, article in symbols:
                a1 = Article(l, d, hl, symbol, article)
                finalListofArticleObjects.append(a1)

        return finalListofArticleObjects

    # prints the article summary
    def print_all_NN_articles(self, x):
        for r in range(len(x)):
            print(x[r].toString)
            print("-------------------------------------------------------------------------------------------------\n")


class PersistScrapeResults(Service):
    def __init__(self, scrape_request, scrape_results):
        self.scrape_request = scrape_request
        self.scrape_results = scrape_results
        self.created_results = []
        self.updated_results = []

    def process(self):
        for result in self.scrape_results:
            # Look for existing scrape result based on uniqueness (what is that?)
            scrape_result = ScrapeResult.objects.filter(
                user=self.scrape_request.user,
                symbol=Symbol.objects.get_or_create(name=result.symbol)[0],
                headline=result.headline,
                posted_at=result.posted_at,
            ).first()
            if scrape_result is None:
                scrape_result = ScrapeResult.objects.create(
                    user=self.scrape_request.user,
                    scrape_request=self.scrape_request,
                    symbol=Symbol.objects.get_or_create(name=result.symbol)[0],
                    headline=result.headline,
                    posted_at=result.posted_at,
                )
            # Update the ScrapeResult
            scrape_result.article = result.article
            scrape_result.save()
        self.scrape_request.scrape_did_complete()
