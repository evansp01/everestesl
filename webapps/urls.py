from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^', include('everest.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^search/', include('haystack.urls')),
                       )
