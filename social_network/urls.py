from django.conf.urls import patterns, url
from . import views

# Define the URLS that we are using
urlpatterns = patterns('',
                       (r'^accounts/profile/$', views.redirect_user),
                       # Actual view urls
                       url(r'^accounts/(?P<page_owner>\w+)/$',
                           views.profile_view, name='profile_view'),
                       url(r'^accounts/(?P<page_owner>\w+)/(?P<sub_page>\w+)/$',
                           views.profile_view, name='page_view'),
                       url(r'^messages/$', views.messages_view,
                           name='messages_view'),
                       url(r'^employee/$', views.employee_view,
                           name='employee_view'),
                       url(r'^manager/$', views.manager_view,
                           name='manager_view'),
                       # Non-visual ajax urls
                       # Employee Stuff
                       url(r'^manager/list-all-employees/$', views.list_all_employees_ajax,
                           name='list_all_employees'),
                       # Customer and other
                       url(r'^accounts/submit-post/$', views.submit_post_ajax,
                           name='submit_post'),
                       url(r'^accounts/submit-comment/$', views.submit_comment_ajax,
                           name='submit_comment'),
                       url(r'^accounts/submit-like/$', views.submit_like_ajax,
                           name='like_post'),
                       url(r'^employee/create-advertisement/$', views.create_advertisement_ajax,
                           name='create_advertisement'),
                       url(r'^employee/delete-advertisement/$', views.delete_advertisement_ajax,
                           name='delete_advertisement'),
                       url(r'^employee/produce-list-of-all-items-advertised/$', views.produce_list_of_all_items_advertised_ajax,
                           name='produce_list_of_all_items_advertised'),
                       url(r'^employee/generate-mailing-list/$', views.generate_mailing_list_ajax,
                           name='generate_mailing_list'),
                       url(r'^employee/list-all-customers/$', views.list_all_customers_ajax,
                           name='list_all_customers'),
                       url(r'^employee/delete-customer/$', views.del_customer_ajax,
                           name='delete_customer'),
                       url(r'^employee/update-customer/$', views.update_customer_ajax,
                           name='update_customer'),

                       url(r'^employee/list-item-suggestions/$', views.list_item_suggestions_ajax,
                           name='list_item_suggestions'),

                       url(r'^messages/get_messages/$', views.get_messages_ajax,
                           name='messages'),
                       url(r'^get_friends/$', views.get_friends_ajax,
                           name='friends'),
                       url(r'^list/$', views.list_view, name='list'),
                       url(r'^create_account/$',
                           views.create_account_view, name='list'),
                       url(r'^create_employee_account/$',
                           views.create_employee_account_view, name='list'),
                       url(r'^logout/$', views.logout_view, name='list'),
                       url(r'^$', views.redirect_to_home),
                       )
