from django.conf.urls import patterns, url

import views
import views_game
import views_user
import views_admin
import views_ws

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

     url(r'^((?P<lang>[\w-]+)/)?$', views.index, name='index'),

     url(r'^((?P<lang>[\w-]+)/)?user$', views_user.index),
     url(r'^((?P<lang>[\w-]+)/)?user/logout$', views_user.logout, name="user.logout"),

     url(r'^((?P<lang>[\w-]+)/)?user/nickname$', views_user.nickname, name="user.nickname"),
     url(r'^((?P<lang>[\w-]+)/)?user/avis$', views_user.avis, name="user.avis"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquesta1$', views_user.enquesta1, name="user.enquesta1"),
     url(r'^((?P<lang>[\w-]+)/)?user/enquesta2$', views_user.enquesta2, name="user.enquesta2"),

     url(r'^((?P<lang>[\w-]+)/)?user/registre', views_user.registre, name="user.registre"),
     url(r'^((?P<lang>[\w-]+)/)?user/story', views_user.story, name="user.story"),
     url(r'^((?P<lang>[\w-]+)/)?user/narrative', views_user.narrative, name="user.narrative"),

     url(r'^((?P<lang>[\w-]+)/)?user/final_joc', views_user.final_joc, name="user.final_joc"),

     url(r'^((?P<lang>[\w-]+)/)?user/public_goods1', views_user.public_goods1, name="user.public_goods1"),

     url(r'^((?P<lang>[\w-]+)/)?admin$', views_admin.registre, name='admin.admin'),
     url(r'^((?P<lang>[\w-]+)/)?admin/registre$', views_admin.registre, name='admin.registre'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida$', views_admin.partida, name='admin.partida'),
     url(r'^((?P<lang>[\w-]+)/)?admin/stats$', views_admin.stats, name='admin.stats'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users$', views_admin.users, name='admin.users'),
     url(r'^((?P<lang>[\w-]+)/)?admin/users/reset/(?P<user_id>\d+)$', views_admin.users_reset, name='admin.users_reset'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida_list$', views_admin.partida_list, name='admin.partida_list'),
     url(r'^((?P<lang>[\w-]+)/)?admin/partida_detail/(?P<num_partida>\d+)/$', views_admin.partida_detail, name='admin.partida_detail'),

     url(r'^((?P<lang>[\w-]+)/)?ws/tancar_partida/(?P<num_partida>\d+)/', views_ws.tancar_partida, name='ws.tancar_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/usuaris_registrats/', views_ws.usuaris_registrats, name='ws.usuaris_registrats'),
     url(r'^((?P<lang>[\w-]+)/)?ws/estat_partida/', views_ws.estat_partida, name='ws.estat_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/llistat_partides/', views_ws.llistat_partides, name='ws.llistat_partides'),
     url(r'^((?P<lang>[\w-]+)/)?ws/stats_partida/', views_ws.stats_partida, name='ws.stats_partida'),
     url(r'^((?P<lang>[\w-]+)/)?ws/stats_partida_detail/(?P<num_partida>\d+)/', views_ws.stats_partida_detail, name='ws.stats_partida_detail'),

     url(r'^((?P<lang>[\w-]+)/)?ws/demanar_dades/(?P<user_id>\d+)/', views_ws.demanar_dades, name='ws.demanar_dades'),

     url(r'^((?P<lang>[\w-]+)/)?ws/send_action_public_goods/(?P<user_id>\d+)/(?P<result>[\w-]+)',views_ws.send_action_public_goods, name='ws.send_action_public_goods'),
     url(r'^((?P<lang>[\w-]+)/)?ws/get_results_public_goods/(?P<game_id>\d+)/(?P<user_id>\d+)',views_ws.get_results_public_goods, name='ws.get_results_public_goods'),

)
