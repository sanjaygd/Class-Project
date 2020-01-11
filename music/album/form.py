from django import forms
from .models import Album,Singer,Song,Vote,AlbumVote,AlbumComment

import multi_form


class AlbumForm(forms.ModelForm):
    title = forms.CharField(max_length=25,label='Album Title')
    class Meta:
        model=Album
        fields = ['title','discription']


class SingerForm(forms.ModelForm):

    class Meta:
        model = Singer
        fields = ['first_name', 'last_name']
        


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title','language']



class SongVoteForm(forms.ModelForm):
    like = forms.ChoiceField(widget=forms.RadioSelect,choices=Vote.VALUE_CHOICE)

    class Meta:
        model = Vote
        fields = ['like',]


class AlbumVoteForm(forms.ModelForm):

    class Meta:
        model = AlbumVote
        fields = ['like']


class AlbumCommentForm(forms.ModelForm):

    class Meta:
        model = AlbumComment
        fields = ['comment']