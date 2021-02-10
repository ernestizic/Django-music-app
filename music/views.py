from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .models import Album, Song, SongComment
from .forms import SongCommentForm
from django.db.models import Q


# Create your views here.

# View function for album list and album details
def index(request):
    albums = Album.objects.all()
    query = request.GET.get('q')
    if query:
        albums = Album.objects.filter(
            Q(artist__icontains=query) |
            Q(album_title__icontains=query)
        )
    return render(request, 'music/index.html', {'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)  # album = Album.objects.get(pk=album_id)
    return render(request, 'music/album_detail.html', {'album': album})


# View functions for song list and song detail
def song_list(request):
    song_list = Song.objects.all().order_by('artist')
    latest_songs = Song.objects.all()[:5:2]
    context = {
        'song_list': song_list,
        'latest_songs': latest_songs,
    }
    return render(request, 'music/song_list.html', context)


def song_detail(request, id, slug):
    song = get_object_or_404(Song, id=id, slug=slug)  # song = Song.objects.get(slug=slug)
    comments = SongComment.objects.filter(song=song, reply=None).order_by('-id')
    is_liked = False
    if song.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = SongCommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = SongComment.objects.get(id=reply_id)
            comment = SongComment.objects.create(song=song, user=request.user, content=content, reply=comment_qs)
            comment.save()
            # return HttpResponseRedirect(song.get_absolute_url())
    else:
        comment_form = SongCommentForm()

    context = {
        'song': song,
        'is_liked': is_liked,
        'total_likes': song.total_likes(),
        'comments': comments,
        'comment_form': comment_form,

    }
    if request.is_ajax():
        html = render_to_string('music/song_comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'music/song_detail.html', context)


# View function for liking a particular song
def like_song(request):
    # song = get_object_or_404(Song, id=request.POST.get('song_id'))
    song = get_object_or_404(Song, id=request.POST.get('id'))
    is_liked = False
    if song.likes.filter(id=request.user.id).exists():
        song.likes.remove(request.user)
        is_liked = False
    else:
        song.likes.add(request.user)
        is_liked = True
    context = {
        'song': song,
        'is_liked': is_liked,
        'total_likes': song.total_likes,
    }
    if request.is_ajax():
        html = render_to_string('music/song_like_section.html', context, request=request)
        return JsonResponse({'form': html})


def search(request):
    albums = Album.objects.all()
    songs = Song.objects.all()
    query = request.GET.get('q')
    if query:
        albums = Album.objects.filter(
            Q(artist__icontains=query) |
            Q(album_title__icontains=query)
        )
    if query:
        songs = Song.objects.filter(
            Q(artist__icontains=query) |
            Q(song_title__icontains=query)
        )
    context = {
        'albums': albums,
        'songs': songs
    }
    return render(request, 'music/search.html', context)
