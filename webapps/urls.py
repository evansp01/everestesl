from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webapps.views.home', name='home'),
                       url(r'^', include('everest.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       )  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
