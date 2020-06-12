"""
Цель: Список urlpatterns направляет URL-адреса к представлениям 
Автор: Немашкало Александр
"""


from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('apipy/admin/', admin.site.urls),
    path('apipy/twitter/', include('twitter_parsing.urls')),
    path('apipy/auth/', include('djoser.urls')),
    path('apipy/auth/', include('djoser.urls.authtoken')),
]
