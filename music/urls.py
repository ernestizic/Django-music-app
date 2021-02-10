from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    # URL patterns for album list and album details
    path('', views.index, name='index'),  # Album list
    path('<int:album_id>/', views.album_detail, name='album_detail'),

    # URL patterns for song list and song details
    path('songs/', views.song_list, name='song_list'),
    re_path('(?P<id>[0-9])/(?P<slug>[\w-]+)/', views.song_detail, name='song_detail'),

    # URL pattern for liking a song
    path('like/', views.like_song, name='like_song'),

    # URL pattern for search bar
    path('search/', views.search, name='search'),
]
