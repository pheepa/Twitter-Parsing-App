from django.contrib import admin
from .models import TweetAccount,TweetInquiry,Inquiry,Writing ,Account

admin.site.register(Inquiry)
admin.site.register(TweetAccount)
admin.site.register(TweetInquiry)
admin.site.register(Writing)
admin.site.register(Account)