from django.conf.urls import patterns, url
from . import views

# Define the URLS that we are using
urlpatterns = patterns('',
                       (r'^accounts/profile/$', views.redirect_user),
                       # Actual view urls
                       url(r'^accounts/(?P<username>\w+)/$',
                           views.profile_view, name='profile_view'),
                       url(r'^messages/$', views.messages_view,
                           name='messages_view'),
                       # Non-visual ajax urls
                       url(r'^accounts/submit-post/$', views.submit_post_ajax,
                           name='submit_post'),
                       url(r'^messages/get_messages/$', views.get_messages_ajax,
                           name='messages'),
                       url(r'^get_friends/$', views.get_friends_ajax,
                           name='friends'),
                       url(r'^list/$', views.list_view, name='list'),
                       url(r'^logout/$', views.logout_view, name='list'),
                       url(r'^$', views.redirect_to_home),
                       )
