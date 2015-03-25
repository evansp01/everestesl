from django.conf.urls import patterns, include, url

urlpatterns = patterns('everest.views',
    url(r'^$', 'general.home',name='yolo'),
    # Route for built-in authentication with our own custom login page
#    url(r'^register$', 'register'),
#    url(r'^confirm/(?P<username>[a-zA-Z0-9_\-\.]*)/(?P<token>[a-z0-9\-]+)$','confirm'),
)

urlpatterns += patterns('everest.views.general',
    url(r'^find_list$','find_list',name='find_list'),
    url(r'^find_user$','find_user',name='find_user'),
    url(r'^find_sentence$','find_sentence',name='find_sentence'),
    url(r'^manage_account$','manage_account',name='manage_account')
)

urlpatterns += patterns('everest.views.teacher',
    url(r'^teacher$','home',name='teacher_home'),
    url(r'^teacher/add_list$','add_list',name='add_list'),
    url(r'^teacher/my_lists$','user_lists',name='user_lists'),
    url(r'^teacher/profile$','profile',name='teacher_profile')
)

urlpatterns += patterns('everest.views.translator',
    url(r'^translator$','home',name='translator_home'),
    url(r'^translator/need_translation$','need_translation',name='need_translation'),
    url(r'^translator/need_audio$','need_audio',name='need_audio'),
    url(r'^transtator/profile$','profile',name='translator_profile')
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'everest/login.html'}),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)