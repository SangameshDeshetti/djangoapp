from django.conf.urls import url
from .views import home_view, fetch_transactions

urlpatterns = [
    # Home page
    url(r'^$', home_view, name="home"),

    # Date filter url to fetch data
    url(r'get_transactions/$', fetch_transactions),
]
