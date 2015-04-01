from django.conf.urls import patterns, include, url
from django.contrib import admin
from api import urls

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^api/', include('api.urls', namespace='api', app_name='api')),

)