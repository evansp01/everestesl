from django.conf.urls import patterns, include, url

urlpatterns = patterns('everest.views',
                       url(r'^$', 'general.home', name='home'),
                       # Route for built-in authentication with our own custom login page
                       url(r'^register$', 'general.register', name='register'),
                       # url(r'^confirm/(?P<username>[a-zA-Z0-9_\-\.]*)/(?P<token>[a-z0-9\-]+)$','confirm'),
                       )

urlpatterns += patterns('everest.views.general',
                        url(r'^lessons/my$', 'find_my_lessons', name='find_my_lessons'),
                        url(r'^lessons/(?P<userid>[0-9]+)/$', 'find_lesson', name='find_lesson'),
                        url(r'^users/all$', 'all_users', name='all_users'),
                        url(r'^sentences/all$', 'all_sentences', name='all_sentences'),
                        url(r'^lesson/(?P<lesson>[0-9]+)$', 'view_lesson', name='view_lesson'),
                        url(r'^user/(?P<username>.*)$', 'view_user', name='view_user'),
                        url(r'^manage_account$', 'manage_account', name='manage_account'),
                        )

urlpatterns += patterns('everest.views.teacher',
                        url(r'^teacher$', 'home', name='teacher_home'),
                        url(r'^teacher/create_lesson$', 'create_lesson', name='create_lesson'),
                        url(r'^teacher/edit_lesson/(?P<lesson>[0-9]+)$', 'edit_lesson', name='edit_lesson')
                        )

urlpatterns += patterns('everest.views.translator',
                        url(r'^translator$', 'home', name='translator_home'),
                        url(r'^translator/need_translation$', 'need_translation', name='need_translation'),
                        url(r'^translator/need_audio$', 'need_audio', name='need_audio')
                        )
urlpatterns += patterns('everest.views.sentence',
                        url(r'^sentence/(?P<sentence>[0-9]+)$', 'view_sentence', name='view_sentence'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/record/english$', 'record_english', name='record_english'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/record/nepali$', 'record_nepali', name='record_nepali'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/recording$', 'upload_audio', name='submit_recording'),
                        url(r'^sentence/(?P<sentence>[0-9]+)/translation$', 'submit_translation',
                            name='submit_translation'),
                        url(r'^audio/english/(?P<audio>[0-9]+)$', 'english_audio', name='english_audio'),
                        url(r'^audio/nepali/(?P<audio>[0-9]+)$', 'nepali_audio', name='nepali_audio'),
                        )

urlpatterns += patterns('everest.views.delete',
                        url(r'^delete-translation/(?P<translation>[0-9]+)$', 'del_translation', name='del_translation'),
                        url(r'^delete-englishaudio/(?P<audio>[0-9]+)$', 'del_englishaudio', name='del_englishaudio'),
                        url(r'^delete-nepaliaudio/(?P<audio>[0-9]+)$', 'del_nepaliaudio', name='del_nepaliaudio'),
                        url(r'^delete-sentence/(?P<sentence>[0-9]+)/(?P<lesson>[0-9]+)$', 'del_sentence',
                            name='del_sentence'),
                        url(r'^delete-lesson/(?P<lesson>[0-9]+)$', 'del_lesson', name='del_lesson')
                        )

urlpatterns += patterns('everest.views.search',
                        url(r'^ajax/search_sentences$', 'search_sentence', name='search_sentence'),
                        url(r'^lessons/$', 'search_lesson', name='search_lessons'),
                        url(r'^ajax/search_user$', 'search_user', name='search_user'),
                        )

urlpatterns += patterns('',
                        url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'everest/login.html'}),
                        # Route to logout a user and send them back to the login page
                        url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                        )
