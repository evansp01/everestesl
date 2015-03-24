from django.conf.urls import patterns, include, url

urlpatterns = patterns('everest.views',
    url(r'^$', 'main.home'),
    # Route for built-in authentication with our own custom login page
#    url(r'^register$', 'register'),
#    url(r'^confirm/(?P<username>[a-zA-Z0-9_\-\.]*)/(?P<token>[a-z0-9\-]+)$','confirm'),
)

# urlpatterns += patterns('',
#     url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'everest/login.html'}),
#     # Route to logout a user and send them back to the login page
#     url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
#     )