from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # For using static files
from django.conf.urls.static import static  # For using static files
from django.conf import settings  # For using media files
from music import views as music_views  # For importing music views to use as index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', music_views.index, name='home'),  # To remove in the future
    path('accounts/', include('accounts.urls')),
    path('music/', include('music.urls')),

    # Password reset Urls
    path('', include('django.contrib.auth.urls')),

    # url for redirecting to the appropriate oath application which the social websites provides
    path('oauth/', include('social_django.urls', namespace='social')),
]

# static files
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
