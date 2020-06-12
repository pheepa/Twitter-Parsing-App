from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Inquiry(models.Model):
    """
    Цель: описать класс модели, которая будет хранится в базе данных
    Автор: Немашкало Александр
    """
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hashtag = models.CharField("хэштег", max_length=100)
    date = models.DateTimeField('Дата запроса', default=timezone.now)
    number_tweets = models.IntegerField("количество твитов")
    result_negative = models.IntegerField("уровень негатива в процентах", blank=True)
    from_date = models.DateField('с ')
    until_date = models.DateField('до')


class Account(models.Model):
    """
    Цель: Описать модель Аккаунта для парсинга
    Автор: Немашкало Александр
    """
    objects = models.Manager()
    name = models.TextField("Название")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("дата публикации", default=timezone.now)
    negative = models.IntegerField("уровень негатива в процентах", blank=True, default=50)
    number_tweets = models.IntegerField("количество твитов", default=0)


class TweetAccount(models.Model):
    """
    Цель: Описать модель твита, спарсенного через аккаунт
    Автор: Немашкало Александр
    """
    objects = models.Manager()
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='Atweets', )
    text = models.TextField("текст твита")
    negative = models.BooleanField("сентимент", blank=True)


class TweetInquiry(models.Model):
    """
    Цель: Описать модель твита спарсенного через хештег
    Автор: Немашкало Александр
    """
    objects = models.Manager()
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='Itweets', )
    text = models.TextField("текст твита")
    negative = models.BooleanField("сентимент", blank=True)


class Writing(models.Model):
    """
    Цель: Описать модель теста,создаваемого пользователем для проверки
    Автор: Немашкало Александр
    """
    objects = models.Manager()
    title = models.TextField("Название")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("текст")
    date = models.DateTimeField("дата публикации", default=timezone.now)
    negative = models.BooleanField("негатив", blank=True, default=False)
