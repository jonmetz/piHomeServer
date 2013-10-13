from django.conf.urls import patterns, include, url
# import models
from MediaCenter.models import *
from MediaCenter.views import *


urlpatterns = patterns('',
    url(r'^$', media_center),
    url(r'^MusicLibrary/$', music_library),
    url(r'^MusicLibrary/play/([A-Za-z0-9\.\-_]+)/', music_player),
)
