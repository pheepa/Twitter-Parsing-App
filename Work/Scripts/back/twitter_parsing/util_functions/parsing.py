import sys
import re


from twitter_scraper.query import query_tweets, query_tweets_from_user

import datetime as dt

import numpy as np
import matplotlib.pyplot as plt


from predict import predictor



class Parser():
    def __init__(self, predictor):
    	"""
	Цель: Парсинг твиттера и построение графиков
	Вход: self, predictor
	Выход:
	Автор: Абаполов Филипп

    	"""
        self.query = ''
        self.today = dt.date.today()
        self.yesterday = dt.date.today() - dt.timedelta(days=1)
        self.lang = 'english'
        self.predictor = predictor

        self.tweets = []
        self.sentiments = []

    def __parse(self, from_date, until_date, query, limit, mode="user"):
    	"""
    	Цель: Парсинг твиттера по запросу
	Вход: self, from_date, until_date, query, limit, mode="user" - начальная дата, конечная дата, запрос, лимит и мод парсинга user/hashtag
	Выход:
	Автор: Абаполов Филипп

    	"""
        self.sentiments = []
        self.tweets = []
        self.query = query
        if mode == "hashtag":
            query = "#" + query
            q_t = query_tweets(query=self.query, begindate=from_date, enddate=until_date,
                               limit=limit, lang=self.lang)

        else:
            q_t = query_tweets_from_user(query, limit)

        for t in q_t[:limit]:
            self.tweets.append(str(t.text.encode('utf-8').decode('ISO-8859-1')))


    def predict_user(self, from_date=dt.date.today() - dt.timedelta(days=1),
                     until_date=dt.date.today(), query='potus', limit=5, mode="user"):
        """
        Цель: Парсинг твиттера по запросу
	Вход: self, from_date=dt.date.today() - dt.timedelta(days=1), until_date=dt.date.today(), query='potus', limit=5, mode="user"
	 - начальная дата, конечная дата, запрос, лимит и мод парсинга u 
	Выход:self.tweets
	Автор: Абаполов Филипп

        """
        self.__parse(from_date, until_date, query, limit, mode)

        return self.tweets

    def predict_hashtag(self, from_date=dt.date.today() - dt.timedelta(days=1),
                        until_date=dt.date.today(), query='potus', limit=5):
        """
        Цель: Парсинг твиттера по запросу
	Вход: self, from_date=dt.date.today() - dt.timedelta(days=1), until_date=dt.date.today(), query='potus', limit=5
	 - начальная дата, конечная дата, запрос, лимит и мод парсинга u 
	Выход:self.tweets
	Автор: Абаполов Филипп

        """
        self.__parse(from_date, until_date, query, limit, mode="hashtag")

        return self.tweets

    def plot(self, query, mode='user', last_days=1, limit=100):
    	"""
    	Цель: Парсинг твиттера по запросу
	Вход: self, query, mode='user', last_days=1, limit=100 - запрос, мод hashtag/user, количество последних дней, лимит
	Выход:
	Автор: Абаполов Филипп

    	"""
        last_days = int(last_days)
        from_date = self.today - dt.timedelta(days=last_days)
        until_date = self.today

        self.predict_user(from_date, until_date, query, limit, mode)

        for t in self.tweets:  # new
            self.sentiments.append(self.predictor.predict_one_sample(t))  # new

        f = plt.figure(figsize=(8, 6))
        # 300 represents number of points to make between T.min and T.max

        plt.plot(self.sentiments)
        if mode == "user":
            f.suptitle('Sentiment analysis of {} {} on last {} tweets '.format(query, mode, len(self.sentiments)))
        else:
            f.suptitle('Sentiment analysis of {} {} from {}, to {}'.format(query, mode, from_date, until_date))
        plt.xlabel('tweets')
        plt.ylabel('percentage of positive')
        plt.savefig(sys.path[2] + "/Graphics/plot_{}.png".format(mode))


parser = Parser(predictor)
