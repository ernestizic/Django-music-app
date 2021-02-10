from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

# Album Model
class Album(models.Model):
    artist = models.CharField(max_length=200)
    album_title = models.CharField(max_length=250)
    album_logo = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.album_title + ' - ' + self.artist

    def get_absolute_url(self):
        return reverse('music:album_detail', args=[self.id])


# Song Model
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    artist = models.CharField(max_length=200)
    song_title = models.CharField(max_length=250)
    slug = models.SlugField()
    cover_photo = models.ImageField(default='default.png', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.song_title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('music:song_detail', args=[self.id, self.slug])


# Song Comments Model
class SongComment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    reply = models.ForeignKey('SongComment', null=True, related_name='replies', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.song.song_title + ' - ' + self.user.username

