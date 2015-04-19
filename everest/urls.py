from django.conf.urls import patterns, url

# TODO: Move lesson / users stuff all to search since it has a search bar
urlpatterns = patterns('everest.views.general',
                       url(r'^lessons/my$', 'find_my_lessons', name='find_my_lessons'),
                       url(r'^lessons/(?P<userid>[0-9]+)/$', 'find_lesson', name='find_lesson'),
                       url(r'^lesson/(?P<lesson>[0-9]+)$', 'view_lesson', name='view_lesson'),
                       url(r'^user/(?P<username>[a-zA-Z0-9_]+)$', 'view_user', name='view_user'),
                       url(r'^user/$', 'view_self', name='view_self'),
                       url(r'^register$', 'register', name='register'),
                       url(r'^$', 'home', name='home'),
                       )

urlpatterns += patterns('everest.views.teacher',
                        url(r'^teacher$', 'home', name='teacher_home'),
                        url(r'^teacher/create_lesson$', 'create_lesson', name='create_lesson'),
                        url(r'^teacher/edit_lesson/(?P<lesson>[0-9]+)$', 'edit_lesson', name='edit_lesson'),
                        url(r'^teacher/add_sentence/(?P<sentence>[0-9]+)/(?P<lesson>[0-9]+)$', 'add_sentence',
                            name='add_sentence'),
                        )

urlpatterns += patterns('everest.views.translator',
                        url(r'^translator$', 'home', name='translator_home'),
                        url(r'^translator/need_translation$', 'need_translation', name='need_translation'),
                        url(r'^translator/need_audio$', 'need_audio', name='need_audio')
                        )

urlpatterns += patterns('everest.views.profile',
                        url(r'^manage_account$', 'manage_account', name='manage_account'),
                        url(r'^ajax/change_personal$', 'change_personal', name='change_personal'),
                        url(r'^ajax/change_password$', 'change_password', name='change_password'),
                        url(r'^ajax/change_picture$', 'change_picture', name='change_picture'),
                        )

urlpatterns += patterns('everest.views.sentence',
                        url(r'^sentence/(?P<sentence>[0-9]+)$', 'view_sentence', name='view_sentence'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/record/english$', 'record_english', name='record_english'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/record/nepali$', 'record_nepali', name='record_nepali'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/recording$', 'upload_audio', name='submit_recording'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/translation$', 'submit_translation',
                            name='submit_translation'),
                        )

urlpatterns += patterns('everest.views.delete',
                        url(r'^delete/translation/(?P<translation>[0-9]+)$', 'del_translation', name='del_translation'),
                        url(r'^delete/english_audio/(?P<audio>[0-9]+)$', 'del_englishaudio', name='del_englishaudio'),
                        url(r'^delete/nepali_audio/(?P<audio>[0-9]+)$', 'del_nepaliaudio', name='del_nepaliaudio'),
                        url(r'^delete/sentence/(?P<sentence>[0-9]+)/(?P<lesson>[0-9]+)$', 'del_sentence',
                            name='del_sentence'),
                        url(r'^delete-lesson/(?P<lesson>[0-9]+)$', 'del_lesson', name='del_lesson')
                        )

urlpatterns += patterns('everest.views.search',
                        url(r'^sentences/$', 'search_sentence', name='search_sentences'),
                        url(r'^lessons/$', 'search_lesson', name='search_lessons'),
                        url(r'^users/$', 'search_user', name='search_users'),
                        )

urlpatterns += patterns('',
                        url(r'^login$', 'django.contrib.auth.views.login',
                            {'template_name': 'everest/signin_register/login.html'}),
                        # Route to logout a user and send them back to the login page
                        url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                        )
