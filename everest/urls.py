from django.conf.urls import patterns, include, url

urlpatterns = patterns('everest.views',
    url(r'^$', 'general.home',name=''),


    # Route for built-in authentication with our own custom login page
#    url(r'^register$', 'register'),
#    url(r'^confirm/(?P<username>[a-zA-Z0-9_\-\.]*)/(?P<token>[a-z0-9\-]+)$','confirm'),
)

urlpatterns += patterns('everst.views.general',
    url(r'^fild_list$','general.find_list',name='find_list'),
    url(r'^fild_user$','general.find_user',name='find_user'),
    url(r'^fild_sentence$','general.find_sentence',name='find_sentence'),
    url(r'^manage_account$','general.manage_account',name='manage_account')
)

# urlpatterns += patterns('',
#     url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'everest/login.html'}),
#     # Route to logout a user and send them back to the login page
#     url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
#     )