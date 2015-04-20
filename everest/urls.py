from django.conf.urls import patterns, url

urlpatterns = patterns('everest.views.general',
                       url(r'^lesson/(?P<lesson>[0-9]+)$', 'view_lesson', name='view_lesson'),
                       url(r'^profile/(?P<username>[a-zA-Z0-9_]+)$', 'view_user', name='view_user'),
                       url(r'^profile/$', 'view_self', name='view_self'),
                       url(r'^register$', 'register', name='register'),
                       url(r'^$', 'home', name='home'),
                       )

urlpatterns += patterns('everest.views.teacher',
                        url(r'^teacher/create-lesson$', 'create_lesson', name='create_lesson'),
                        url(r'^teacher/edit-lesson/(?P<lesson>[0-9]+)$', 'edit_lesson', name='edit_lesson'),
                        url(r'^teacher/add-sentence/(?P<sentence>[0-9]+)/(?P<lesson>[0-9]+)$', 'add_sentence',
                            name='add_sentence'),
                        )

urlpatterns += patterns('everest.views.profile',
                        url(r'^manage_account$', 'manage_account', name='manage_account'),
                        url(r'^ajax/change-personal$', 'change_personal', name='change_personal'),
                        url(r'^ajax/change-password$', 'change_password', name='change_password'),
                        url(r'^ajax/change-picture$', 'change_picture', name='change_picture'),
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
                        url(r'^delete/english-audio/(?P<audio>[0-9]+)$', 'del_englishaudio', name='del_englishaudio'),
                        url(r'^delete/nepali-audio/(?P<audio>[0-9]+)$', 'del_nepaliaudio', name='del_nepaliaudio'),
                        url(r'^delete/sentence/(?P<sentence>[0-9]+)/(?P<lesson>[0-9]+)$', 'del_sentence',
                            name='del_sentence'),
                        url(r'^delete-lesson/(?P<lesson>[0-9]+)$', 'del_lesson', name='del_lesson')
                        )

urlpatterns += patterns('everest.views.search',
                        url(r'^sentences/$', 'search_sentences', name='search_sentences'),
                        url(r'^sentences/needs-translation$', 'search_needs_translation',
                            name='search_needs_translation'),
                        url(r'^sentences/needs-english-audio$', 'search_needs_engaudio', name='search_needs_engaudio'),
                        url(r'^sentences/needs-nepali-audio$', 'search_needs_nepaudio', name='search_needs_nepaudio'),
                        url(r'^lessons/$', 'search_lessons', name='search_lessons'),
                        url(r'^lessons/(?P<username>[a-zA-Z0-9_]+)$', 'search_user_lessons',
                            name='search_user_lessons'),
                        url(r'^lessons/my-lessons', 'search_my_lessons', name='search_my_lessons'),
                        url(r'^users/$', 'search_users', name='search_users'),
                        )

urlpatterns += patterns('',
                        url(r'^login$', 'django.contrib.auth.views.login',
                            {'template_name': 'everest/signin_register/login.html'}),
                        # Route to logout a user and send them back to the login page
                        url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
                        )
