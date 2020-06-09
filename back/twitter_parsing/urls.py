
from django.urls import path
from .views import InquiryCreateView ,InquiryDetailView, GetInquiriesView
from .views import WritingCreateView, WritingListView, WritingDetailView
from .views import UserCreate, LoginView
from .views import AccountCreateView, GetAccountsView, AccountDetailView
from .views import ChartingAccount, ChartingHashtag





urlpatterns = [
    path('inquiry/create/', InquiryCreateView.as_view()),
    path('inquiry/detail/<int:pk>/', InquiryDetailView.as_view()),
    path('inquiry/all/', GetInquiriesView.as_view()),

    path('writing/create/', WritingCreateView.as_view()),
    path('writing/all/', WritingListView.as_view()),
    path('writing/detail/<int:pk>/', WritingDetailView.as_view()),

    path('user/create/', UserCreate.as_view(), name="user_create"),
    path('login/', LoginView.as_view(), name="login"),

    path('charting/account/', ChartingAccount.as_view(), name="charting_account"),
    path('charting/hashtag/', ChartingHashtag.as_view(), name="charting_hashtag"),

    path('account/create/', AccountCreateView.as_view()),
    path('account/all/', GetAccountsView.as_view()),
    path('account/detail/<int:pk>/', AccountDetailView.as_view()),
]
