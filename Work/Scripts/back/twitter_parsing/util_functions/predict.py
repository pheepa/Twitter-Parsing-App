
import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from string import punctuation
import itertools

import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn

import sys
from train import initializer


class Predictor():
    def __init__(self, initializer):
        
        """
        Цель: Получение модели из initializer, обработка текста и предсказываение
	Вход: self, initializer
	Выход:
	Автор: Абаполов Филипп

        """
        
        self.word_to_int = initializer.word_to_int
        self.model = initializer.loaded_net
        self.train_on_gpu = False
        self.batch_size = initializer.batch_size

    def __cleanhtml(self, raw_html):
    	"""
    	Цель: Удаление html тегов из текста 
	Вход: self, raw_html
	Выход:withoutdoublespaces - текст без тегов
	Автор: Абаполов Филипп
	"""
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, ' ', raw_html)
        withoutdoublespaces = re.sub(' +', ' ', cleantext)
        return withoutdoublespaces

    def __tokenize_one_sample(self, sent):
	"""
	Цель: Токенизация
	Вход: self, sent
	Выход:sent - токенизированное предложение
	Автор: Абаполов Филипп

	"""
        lem = WordNetLemmatizer()

        pre_sent = sent.lower()

        # delete punctuation and html tags and numbers
        pre_sent = self.__cleanhtml(pre_sent)
        pre_sent = re.sub('[0-9]+', '', pre_sent)
        pre_sent = re.sub("\'", ' ', pre_sent)
        pre_sent = pre_sent.translate(str.maketrans('', '', punctuation))

        pre_sent = word_tokenize(pre_sent)
        sent = []
        for word in pre_sent:
            word = lem.lemmatize(word)
            if word not in stopwords.words('english'):
                sent.append(word)

        return sent

    def __pad_features_one_sample(self, tweet_int, seq_length=280):
    	"""
    	Цель: Паддинг
	Вход: self, tweet_int, seq_length=280
	Выход:sent - последовательность чисел фиксированной длины
	Автор: Абаполов Филипп

    	"""
        tweet_int = tweet_int[0]
        ## getting the correct rows x cols shape
        features = np.zeros(seq_length, dtype=int)

        ## for each review, I grab that review
        if len(tweet_int):
            features[-len(tweet_int):] = np.array(tweet_int)[:seq_length]

        return features

    def predict_one_sample(self, tweet):
    	"""
    	Цель: Подготовка и определение сентимента текста
	Вход: self, tweet
	Выход:pred.data  - число от 0 до 1 - вероятность того, что текст положительный
	Автор: Абаполов Филипп

    	"""
        self.batch_size = 1
        h = self.model.init_hidden(self.batch_size)

        tweet = self.__tokenize_one_sample(tweet)

        tweet_int = []

        tweet_int.append([self.word_to_int[word] if word in self.word_to_int else 0 for word in tweet])

        inputs = self.__pad_features_one_sample(tweet_int)

        batch = []
        for _ in range(self.batch_size):
            batch.append(inputs)
        inputs = torch.from_numpy(np.array(batch))

        if (self.train_on_gpu):
            inputs = inputs.cuda()

        # Creating new variables for the hidden state, otherwise
        # we'd backprop through the entire training history
        h = tuple([each.data for each in h])

        # get predicted outputs
        output, h = self.model(inputs, h)

        # convert output probabilities to predicted class (0 or 1)
        pred = sum(output) / self.batch_size  # rounds to the nearest integer

        return pred.data


predictor = Predictor(initializer)
