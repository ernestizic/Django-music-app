from django.contrib import admin
from .models import Album, Song, SongComment


# Register your models here.

class SongAdmin(admin.ModelAdmin):
    list_display = ('artist', 'song_title')
    search_fields = ('artist',)
    prepopulated_fields = {'slug': ('artist', 'song_title')}


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('artist', 'album_title')
    search_fields = ('artist', 'album_title')


admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(SongComment)
