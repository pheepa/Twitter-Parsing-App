from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Inquiry, TweetAccount, TweetInquiry, Writing, Account
from django.contrib.auth.models import User

import sys

sys.path.insert(1, 'util_functions')
sys.path.insert(3, '../')
from predict import predictor
from parsing import parser


# Inquiry
class InquiryDetailSerializer(serializers.ModelSerializer):
    """
    Цель: Здесь сериализуется и указываются те поля модели ,которые будут передаваться на front-end
    Автор: Немашкало Александр
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Inquiry
        fields = "__all__"


class InquiryCreateSerializer(serializers.ModelSerializer):
    """
    Цель:В данном классе реализована функция ,которая будет вызываться при создании хештега.
    Автор: Немашкало Александр
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        """
        Цель: Вызывается функция, которая парсит данные из твиттера на основе полученных данных от клиента. Создаются экземпляры класса TweetInquiry 
в базе данных (при каждом добавлении экземпляра вызывается функция, которая будет подсчитывать долю негатива твита). Создается экземпляр класса 
Inquiry в базе данных, при этом перед добавлением экземпляра вызывается функция для вычисления доли негатива данного запроса на основе данных, 
полученных  после добавления и определения доли негатива всех экземпляров класса TweetInquiry
        Вход:self,  validated_data (данные отправленные от Frontend)
        Выход: экземпляр  класса Inquiry (Добавление в бд новых данных )
        Автор: Немашкало Александр
        """
        inquiry = Inquiry()
        inquiry.result_negative = 50
        inquiry.hashtag = validated_data['hashtag']
        inquiry.from_date = validated_data['from_date']
        inquiry.until_date = validated_data['until_date']
        inquiry.number_tweets = validated_data['number_tweets']
        inquiry.user = validated_data['user']
        inquiry.save()

        tweets = parser.predict_hashtag(limit=inquiry.number_tweets, query=inquiry.hashtag,
                                        from_date=inquiry.from_date, until_date=inquiry.until_date)

        npositive = 0.
        for tweet in tweets:
            newTweet = TweetInquiry()
            newTweet.inquiry_id = inquiry.id
            newTweet.text = tweet
            newTweet.negative = predictor.predict_one_sample(tweet=newTweet.text) > 0.5
            if newTweet.negative:
                npositive += 1
            newTweet.save()

        if len(tweets):
            inquiry.result_negative = int(100 * npositive / len(tweets))
        else:
            inquiry.number_tweets = 0
            inquiry.result_negative = -1
        inquiry.save()
        return inquiry

    class Meta:
        model = Inquiry
        fields = "__all__"


# Tweets
class TweetListAccountSerializer(serializers.ModelSerializer):
    """
    Цель:Здесь сериализуются и  указываются те поля модели ,которые будут передаваться на front-end при Get запросе для твита
    Автор: Немашкало Александр
    """
    class Meta:
        model = TweetAccount
        fields = "__all__"


class TweetListInquirySerializer(serializers.ModelSerializer):
    """
    Цель:Здесь сериализуются и  указываются те поля модели ,которые будут передаваться на front-end при Get запросе для твита
    Автор: Немашкало Александр
    """
    class Meta:
        model = TweetInquiry
        fields = "__all__"


class AccountListSerializer(serializers.ModelSerializer):
    """
    Цель:Здесь сериализуется и указываются те поля модели ,которые будут передаваться на front-end при множественном Get запросе для аккаунтов
    Автор: Немашкало Александр
    """
    Atweets = TweetListAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = "__all__"


class InquiryListSerializer(serializers.ModelSerializer):
    """
    Цель:Здесь сериализуется и указываются те поля модели ,которые будут передаваться на front-end при множественном Get запросе для хештегов 
    Автор: Немашкало Александр
    """
    Itweets = TweetListInquirySerializer(many=True, read_only=True)

    class Meta:
        model = Inquiry
        fields = "__all__"


# Account
class AccountCreateSerializer(serializers.ModelSerializer):
    """
    Цель:В данном классе реализована функция ,которая будет вызываться при создании аккаунта твиттера .
    Автор: Немашкало Александр
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        """
        Цель: Вызывается функция, которая парсит данные из твиттера на основе полученных данных от клиента.Создаются экземпляры класса TweetAccount
в базе данных ( при каждом добавлении экземпляра вызывается  функция, которая будет подсчитывать долю негатива твита). Создается экземпляр 
класса Inquiry в базе данных, при этом перед добавлением экземпляра вызывается функция для вычисления доли негатива данного запроса на основе данных, 
полученных  после добавления и определения доли негатива для всех экземпляров класса TweetAccount
        Вход:self,  validated_data (данные отправленные от Frontend)
        Выход: экземпляр  класса Account (Добавление в бд новых данных)
        Автор: Немашкало Александр

        """
        account = Account()
        account.name = validated_data['name']
        account.user = validated_data['user']
        account.number_tweets = validated_data['number_tweets']
        account.save()

        tweets = parser.predict_user(limit=account.number_tweets, query=account.name, mode="user")
        npositive = 0.
        for tweet in tweets:
            newTweet = TweetAccount()
            newTweet.account_id = account.id
            newTweet.text = tweet
            newTweet.negative = predictor.predict_one_sample(tweet=newTweet.text) > 0.5

            if newTweet.negative:
                npositive += 1
            newTweet.save()

        if len(tweets):
            account.negative = int(100 * npositive / len(tweets))
        else:
            account.negative = -1
            account.number_tweets = 0

        account.save()
        return account

    class Meta:
        model = Account
        fields = "__all__"


class AccountDetailSerializer(serializers.ModelSerializer):
    """
    Цель: Здесь сериализуется и указываются те поля модели ,которые будут передаваться на front-end
    Автор: Немашкало Александр
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = "__all__"


# Writing
class WritingDetailSerializer(serializers.ModelSerializer):
    """
    Цель: Здесь указываются те поля модели ,которые будут передаваться на front-end при Delete, Put, Post запросе 
    Автор: Немашкало Александр
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        """
        Цель:Изменение экземпляра класса Writing в базе данных, при этом, перед добавлением экземпляра вызывается функция для  вычисления доли негатива данного текста
        Вход:self,  validated_data (данные отправленные от Frontend)
        Выход: экземпляр  класса Writing(Добавление в бд новых данных)
        Автор: Немашкало Александр
        """
        instance.date = validated_data.get('date', instance.date)
        instance.text = validated_data.get('text', instance.text)
        instance.title = validated_data.get('title', instance.title)
        instance.negative = predictor.predict_one_sample(tweet=instance.text) > 0.5

        instance.save()
        return instance

    def create(self, validated_data):
        """
        Цель:Создается экземпляр класса Writing в базе данных , при этом   перед добавлением экземпляра вызывается функция для  вычисления доли негатива данного текста
        Вход:self, instance, validated_data (данные отправленные от Frontend)
        Выход: экземпляр  класса Writing(Добавление в бд новых данных)
        Автор: Немашкало Александр
        """
        instance = Writing()
        instance.text = validated_data['text']
        instance.title = validated_data['title']
        instance.negative = predictor.predict_one_sample(tweet=instance.text) > 0.5
        instance.user = validated_data['user']
        instance.save()
        return instance

    class Meta:
        model = Writing
        fields = "__all__"


class WritingListSerializer(serializers.ModelSerializer):
    """
    Цель:Здесь сериализуются и  указываются те поля модели ,которые будут передаваться на front-end при множественном Get запросе для текстов 
    Автор: Немашкало Александр
    """
    class Meta:
        model = Writing
        fields = "__all__"


# User
class UserSerializer(serializers.ModelSerializer):
    """
    Цель: Здесь указываются те поля модели ,которые будут передаваться на front-end при работе с моделью User
    Автор: Немашкало Александр
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Цель: Создать пользователя ,добавить данные в бд, создать для этого пользователя токен
        Вход:self,  validated_data (данные отправленные от Frontend)
        Выход: экземпляр  класса User (Добавление в бд новых данных)
        Автор: Немашкало Александр
        """
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
