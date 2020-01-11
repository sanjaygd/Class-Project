from django.db import models
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class Singer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)


    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name )  


class Album(models.Model):
    title = models.CharField(max_length=50)
    discription = models.TextField()
    album_creator = models.ForeignKey(Singer, related_name='sung_by', blank=True,null=True, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
 


    def __str__(self):
        return self.title

    @property
    def songs(self):
        return self.album_name.all()

    @property
    def vote(self):
        return self.albumvote_set.all()

class Song(models.Model):
    song_title = models.CharField(max_length=25)
    album = models.ForeignKey(Album, related_name='album_name', on_delete=models.CASCADE, blank=True)
    singer = models.ManyToManyField(Singer, blank=True)
    language = models.CharField(max_length=25)

    def __str__(self):
        return self.song_title

    
class VoteManager(models.Manager):

    def get_vote_or_unsaved_blank_vote(self,song,user):
        try:
            return Vote.objects.get(song=song,user=user)

        except ObjectDoesNotExist:
            return Vote(song=song,user=user)

class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICE = ((UP, "👍️"),(DOWN, "👎️"),)
    
    
    like = models.SmallIntegerField(null=True, blank=True, choices=VALUE_CHOICE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'song') #this represent user can vote at once for a song He can not vote song again and again

    def __str__(self):
        return '{}-{}-({})'.format(self.song, self.user,self.like)





class AlbumVoteManager(models.Manager):

    def get_vote_or_unsaved_blank_vote(self,album,user):
        try:
            return Vote.objects.get(album=album,user=user)

        except ObjectDoesNotExist:
            return Vote(album=album,user=user)


class AlbumVote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICE = ((UP, "👍️"),(DOWN, "👎️"),)
    
    
    like = models.SmallIntegerField(null=True, blank=True, choices=VALUE_CHOICE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = AlbumVoteManager()

    class Meta:
        unique_together = ('user', 'album') #this represent user can vote at once for a song He can not vote song again and again

    def __str__(self):
        return '{}-{}-({})'.format(self.album, self.user,self.like)




class AlbumCommentManager(models.Manager):

    def get_vote_or_unsaved_blank_vote(self,album,user):
        try:
            return Vote.objects.get(album=album,user=user)

        except ObjectDoesNotExist:
            return Vote(album=album,user=user)


class AlbumComment(models.Model):
    comment = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    commented_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = AlbumCommentManager()

    class Meta:
        unique_together = ('user', 'album') #this represent user can vote at once for a song He can not vote song again and again

    def __str__(self):
        return '{}-{}-({})'.format(self.album, self.user,self.commented_on)