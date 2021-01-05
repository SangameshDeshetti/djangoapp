from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include

urlpatterns = [
    # Admin URLs
    url(r'^admin/', include(admin.site.urls)),

    # Including all URLs of Purchase App
    url(r'^', include('purchase.urls')),
]

# For static URLs
urlpatterns += staticfiles_urlpatterns()
