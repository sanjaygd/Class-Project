from django.contrib import admin
from .models import Album,Singer,Song,Vote,AlbumVote

admin.site.register(Album)
admin.site.register(Singer)
admin.site.register(Song)
admin.site.register(Vote)
admin.site.register(AlbumVote)

