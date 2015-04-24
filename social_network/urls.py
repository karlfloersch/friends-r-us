from django.conf.urls import patterns, url
from . import views

# Define the URLS that we are using
urlpatterns = patterns('',
                       (r'^accounts/profile/$', views.redirect_user),
                       url(r'^accounts/(?P<username>\w+)/$',
                           views.home_view, name='profile_view'),
                       )
