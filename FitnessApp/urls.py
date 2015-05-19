from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
       # grappelli URLS
       (r'^grappelli/',include('grappelli.urls')),
       (r'^tinymce/', include('tinymce.urls')),
       # admin site
       url(r'^', include(admin.site.urls)),
       url(r'^api/', include('api.urls', namespace='api', app_name='api')),
       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
       url(r'^accounts/', include('accounts.urls', namespace='accounts')),
       (r'^tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)