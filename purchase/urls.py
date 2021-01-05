from django.conf.urls import url
from .views import home_view, fetch_transactions
from django.contrib import admin

urlpatterns = [
    url(r'^$', home_view, name="home"),
    url(r'get_transactions/$', fetch_transactions),
]
