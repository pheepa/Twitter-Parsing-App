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
    serializer_class = InquiryCreateSerializer
    permission_classes = (IsAuthenticated,)


class GetInquiriesView(generics.ListAPIView):
    serializer_class = InquiryListSerializer
    queryset = Inquiry.objects.all() 
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return Inquiry.objects.filter(user_id=self.request.user).prefetch_related('Itweets')


class InquiryDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = InquiryDetailSerializer
    queryset = Inquiry.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)  




# Account
class AccountCreateView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer


class GetAccountsView(generics.ListAPIView):
    serializer_class = AccountListSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return Account.objects.filter(user_id=self.request.user).prefetch_related('Atweets')

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)



# Writing
class WritingCreateView(generics.CreateAPIView):
    serializer_class = WritingDetailSerializer


class WritingListView(generics.ListAPIView):
    serializer_class = WritingListSerializer
    queryset = Writing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Writing.objects.filter(user_id=self.request.user)

class WritingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WritingDetailSerializer
    queryset = Writing.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)



# User
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response(
                {"token": user.auth_token.key, "id_user": user.id, 'email': user.email, 'username': username})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ChartingAccount(APIView):
    permission_classes = ()

    def post(self, request, ):
        print('*'*20, sys.path)
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
    permission_classes = ()

    def post(self, request, ):
        title = request.data.get("title")
        days = int(request.data.get("months"))
        parser.plot(last_days=days, mode='hashtag', query=title)
        try:
            f = open(sys.path[2] + '/Graphics/plot_hashtag.png', 'rb')
            image = File(f)
            data = base64.b64encode(image.read())
            f.close()
            return Response({"bits":data})
        except:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


