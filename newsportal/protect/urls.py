import allauth.account.views
from django.urls import path

from .views import IndexView, upgrade_me

urlpatterns = [
    path('index/', IndexView.as_view()),
    path('index/logout/', allauth.account.views.logout),
    path('index/upgrade/', upgrade_me, name='upgrade'),
]