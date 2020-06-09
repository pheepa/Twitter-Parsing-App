from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Inquiry, TweetAccount, TweetInquiry, Writing, Account
from django.contrib.auth.models import User
from django.utils import timezone

# import folder with util functions
import sys
sys.path.insert(1, 'util_functions')
sys.path.insert(3, '../')
from predict import predictor
import datetime
from parsing import parser


# Inquiry
class InquiryDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Inquiry
        fields = "__all__"


class InquiryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):

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
            newTweet.text = tweet[2:-1]
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
    class Meta:
        model = TweetAccount
        fields = "__all__"


class TweetListInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetInquiry
        fields = "__all__"


class AccountListSerializer(serializers.ModelSerializer):
    Atweets = TweetListAccountSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = "__all__"


class InquiryListSerializer(serializers.ModelSerializer):
    Itweets = TweetListInquirySerializer(many=True, read_only=True)

    class Meta:
        model = Inquiry
        fields = "__all__"


# Account
class AccountCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
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
            newTweet.text = tweet[2:-1]
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = "__all__"


# Writing
class WritingDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.text = validated_data.get('text', instance.text)
        instance.title = validated_data.get('title', instance.title)
        instance.negative = predictor.predict_one_sample(tweet=instance.text) > 0.5

        instance.save()
        return instance

    def create(self, validated_data):
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
    class Meta:
        model = Writing
        fields = "__all__"


# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
