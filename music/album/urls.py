from django.urls import path
from . import views
# from .views import  AlbumListView,AlbumDetailView,AlbumCreatView,AlbumDeleteView,AlbumUpdateView,AlbumSinger,SongDetailView




app_name = 'music'
urlpatterns = [
    path('album/',views.AlbumListView.as_view(), name='album_list' ),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='detail_view'),
    path('album/create/',views.AlbumCreatView.as_view(),name='create_view'),
    path('album/delete/<int:pk>/',views.AlbumDeleteView.as_view(),name='delete_view' ),
    path('album/update/<int:pk>/',views.AlbumUpdateView.as_view(),name='update_view'),
    path('album/multi/',views.AlbumSinger.as_view(),name='album_singer_create'),
    path('album/multi/<int:pk>/',views.AlbumSinger.as_view(),name='album_singer'),

    path('album/song/<int:pk>/',views.SongDetailView.as_view(), name='song_detail'),
    path('album/song/create/<int:song_id>/',views.SongVoteCreateView.as_view(), name='song_vote_create'),
    path('album/song/update/<int:song_id>/<int:pk>/', views.SongUpdateView.as_view(), name='song_vote_update')
    
]
