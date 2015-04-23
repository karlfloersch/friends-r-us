from django.conf.urls import patterns, url
from . import views

# Define the URLS that we are using
urlpatterns = patterns('',
                       (r'^home/$', views.home_view),
                       )
