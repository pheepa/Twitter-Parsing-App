"""
Цель: Содержит классы ,которые наследуются от Общих представлений, предоставляемые каркасом REST, которые соответствуют моделям баз данных. 
В классах переопределяются поля, отвечающие за связь с определенной моделью, доступ к представлению и возвращаемые данные . 
В некоторых классах переопределяются и методы. 
Автор: Немашкало Александр
"""

from .serializers import InquiryDetailSerializer, InquiryListSerializer, InquiryCreateSerializer
from .serializers import WritingDetailSerializer, WritingListSerializer
from .serializers import AccountDetailSerializer, AccountListSerializer, AccountCreateSerializer
from .serializers import UserSerializer
from .models import Inquiry, Writing, Account
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from django.http import FileResponse
from django.core.files import File
import base64
import sys

from predict import predictor
from parsing import parser


# Inquiry
class InquiryCreateView(generics.CreateAPIView):
    """
    Цель:Представление, которое обрабатывает Post запрос для Inquiry 
    Автор: Немашкало Александр
    """
    serializer_class = InquiryCreateSerializer
    permission_classes = (IsAuthenticated,)


class GetInquiriesView(generics.ListAPIView):
    """
    Цель:Представление, которое обрабатывает множественный Get запрос для Inquiry 
    Автор: Немашкало Александр
    """
    serializer_class = InquiryListSerializer
    queryset = Inquiry.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        Цель: Сделать так, чтобы пользователю возвращался список только тех запросов ,которые принадлежат ему
        Вход: self
        Выход: отфильтрованный список экземпляров класса Inquiry
        Автор: Немашкало Александр
        """
        return Inquiry.objects.filter(user_id=self.request.user).prefetch_related('Itweets')


class InquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Цель:Представление, которое обрабатывает Put и Delete запрос для Inquiry 
    Автор: Немашкало Александр
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = InquiryDetailSerializer
    queryset = Inquiry.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


# Account
class AccountCreateView(generics.CreateAPIView):
    """
    Цель:Представление, которое обрабатывает Post запрос для Account 
    Автор: Немашкало Александр
    """
    serializer_class = AccountCreateSerializer


class GetAccountsView(generics.ListAPIView):
    """
    Цель:Представление, которое обрабатывает множественный Get запрос для Account
    Автор: Немашкало Александр
    """
    serializer_class = AccountListSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        """
        Цель: Сделать так, чтобы пользователю возвращался список только тех запросов ,которые принадлежат ему
        Вход: self
        Выход: отфильтрованный список экземпляров класса Account
        Автор: Немашкало Александр
        """
        return Account.objects.filter(user_id=self.request.user).prefetch_related('Atweets')


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Цель:Представление, которое обрабатывает Put и Delete запрос для Account
    Автор: Немашкало Александр
    """
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


# Writing
class WritingCreateView(generics.CreateAPIView):
    """
    Цель:Представление, которое обрабатывает Post запрос для Writing 
    Автор: Немашкало Александр
    """
    serializer_class = WritingDetailSerializer


class WritingListView(generics.ListAPIView):
    """
    Цель:Представление, которое обрабатывает множественный Get запрос для Writing
    Автор: Немашкало Александр
    """
    serializer_class = WritingListSerializer
    queryset = Writing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Цель: Сделать так, чтобы пользователю возвращался список только тех запросов ,которые принадлежат ему
        Вход: self
        Выход: отфильтрованный список экземпляров класса Writing
        Автор: Немашкало Александр
        """
        return Writing.objects.filter(user_id=self.request.user)


class WritingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Цель:Представление, которое обрабатывает Put и Delete запрос для Writing
    Автор: Немашкало Александр
    """
    serializer_class = WritingDetailSerializer
    queryset = Writing.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)


# User
class UserCreate(generics.CreateAPIView):
    """
    Цель:Представление, которое обрабатывает запрос с добавлением пользователя
    Автор: Немашкало Александр
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    """
    Цель:Представление, которое обрабатывает запрос с аутентификацией  пользователя
    Автор: Немашкало Александр
    """
    permission_classes = ()

    def post(self, request, ):
        """
        Цель: Проверяет на существование токена в бд и возвращает его, если он есть 
        Вход: self, request (данные из frontend)
        Выход: token,id_user  или  ошибку
        Автор: Немашкало Александр
        """
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response(
                {"token": user.auth_token.key, "id_user": user.id, 'email': user.email, 'username': username})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ChartingAccount(APIView):
    """
    Цель:Представление, которое обрабатывает запрос с созданием графика по аккаунту 
    Автор: Немашкало Александр
    """
    permission_classes = ()

    def post(self, request, ):
        """
        Цель: вызывается функция для  создания  изображения , после чего новое изображение кодируется в байт код , который потом передается  на front-end
        Вход: self, request (данные из frontend)
        Выход:Response (строка из байтов)
        Автор: Немашкало Александр
        """
        name = request.data.get("name")
        limit = int(request.data.get("months"))
        parser.plot(limit=limit, mode='user', query=name)
        try:
            f = open(sys.path[2] + '/Graphics/plot_user.png', 'rb')
            image = File(f)
            data = base64.b64encode(image.read())
            f.close()
            return Response({"bits": data})
        except:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ChartingHashtag(APIView):
    """
    Цель:Представление, которое обрабатывает запрос с созданием графика по хештегу
    Автор: Немашкало Александр
    """
    permission_classes = ()

    def post(self, request, ):
        """
        Цель: вызывается функция для  создания  изображения , после чего новое изображение кодируется в байт код , который потом передается  на front-end
        Вход: self, request (данные из frontend)
        Выход:Response (строка из байтов)
        Автор: Немашкало Александр
        """
        title = request.data.get("title")
        days = int(request.data.get("months"))
        parser.plot(last_days=days, mode='hashtag', query=title)
        try:
            f = open(sys.path[2] + '/Graphics/plot_hashtag.png', 'rb')
            image = File(f)
            data = base64.b64encode(image.read())
            f.close()
            return Response({"bits": data})
        except:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
