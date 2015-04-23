from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^/*', include('social_network.urls', namespace="social_network")),
    url(r'^admin/', include(admin.site.urls)),
]
