from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^/*', include('social_network.urls', namespace="social_network")),
    url(r'^login/$', 'django.contrib.auth.views.login', name="my_login"),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
