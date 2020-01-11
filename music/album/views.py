from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.views.decorators.cache import cache_page


from django.contrib.auth import authenticate,PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView,FormView,View

from .models import Album,Singer,Song,Vote,AlbumVote
from .form import AlbumForm,SingerForm,SongForm,SongVoteForm,AlbumVoteForm,AlbumCommentForm




class SongDetailView(DetailView):
    model = Song
    template_name = 'song/song_detail.html'

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)


        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(song=self.object, user = self.request.user)
            if vote.id:
                vote_url = reverse('music:song_vote_update', kwargs={'song_id':vote.song.id,'pk':vote.id}) #'pk':vote.id
            else:
                vote_url = reverse('music:song_vote_create', kwargs={'song_id':self.object.id}) #

            vote_form = SongVoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_url'] = vote_url
        return ctx



class SongVoteCreateView(LoginRequiredMixin, CreateView):
    form_class = SongVoteForm
    model = Vote
    # fields = ['like']
    

    def get_success_url(self,**kwargs):
        song_id = self.kwargs.get('song_id')
        return reverse('music:song_detail', kwargs={'pk':song_id})
 
    def form_valid(self, form):
        like = form.cleaned_data.get('like')
        user = self.request.user
        song_obj = Song.objects.get(pk=self.kwargs['song_id'])
        vote_obj, created = Vote.objects.get_or_create(song = song_obj, user = user, like=like) 
        form.instance = vote_obj
        return super().form_valid(form)


class SongUpdateView(LoginRequiredMixin, UpdateView):
    form_class = SongVoteForm
    model = Vote

    def get_success_url(self):
        song_id = self.kwargs.get('song_id')
        return reverse('music:song_detail', kwargs={'pk':song_id})


class AlbumSinger(View):
    singer_class = SingerForm
    album_class = AlbumForm
    song_class = SongForm
    template_name = 'album/multi_form_edit.html'
    

    def get(self,request,pk=None):
        if pk:
            
            album_obj = get_object_or_404(Album, pk=pk)
            singer_obj = album_obj.album_creator
            songs = album_obj.album_name.all()

            singer_form = SingerForm(instance=singer_obj)
            album_form = AlbumForm(instance=album_obj)
            song_form = [SongForm(prefix=str(song.id),instance=song)for song in songs]

            context = {
                'singer_form':singer_form,
                'album_form':album_form,
                'song_form':song_form,
            }
            return render(request, self.template_name, context)
        else:
            singer_form = self.singer_class(None)
            album_form = self.album_class(None)
            song_form = [SongForm(instance=Song())]

            context = {
                'singer_form':singer_form,
                'album_form':album_form,
                'song_form':song_form
            }
            return render(request, self.template_name, context)

    def post(self,request,pk=None):
        context = {}
        
        album_obj,created = Album.objects.get_or_create(pk=pk)
        singer_obj = album_obj.album_creator
        songs = album_obj.album_name.all()

        singer_form = SingerForm(request.POST, instance=singer_obj)
        album_form = AlbumForm(request.POST,instance=album_obj)
        song_form = [SongForm(request.POST,instance=song)for song in songs]

        if singer_form.is_valid() and album_form.is_valid() and all([sf.is_valid for sf in song_form]):
            singer_instance = singer_form.save()
            new_album = album_form.save(commit=False)
            new_album.album_creator = singer_instance
            new_album.save()

            for sf in song_form:
                new_song = sf.save(commit=False)
                new_song.album = new_album
                new_song.singer.add(singer_instance) 
                new_song.save()
            return HttpResponseRedirect('/album/')
        context = {
            'singer_form' : singer_form,
            'album_form' : album_form
        }
        return render(request, 'album/multi_form.html', context) 


@method_decorator(cache_page(200), name='dispatch')
class AlbumListView(ListView):
    model = Album
    paginate_by = 5
    
    # print('not cached')
    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)

        # if self.request.user.is_authenticated:
        #     vote = AlbumVote.objects.get_vote_or_unsaved_blank_vote(album=self.object_list.object, user = self.request.user)
        #     if vote.id:
        #         vote_url = reverse('music:album_vote_update', kwargs={'album_id':vote.album.id,'pk':vote.id})
        #     else:
        #         vote_url = reverse('music:album_vote_create', kwargs={'album_id':self.object_list.object.id})


        #     vote_form = AlbumVoteForm(instance=vote)
        #     ctx['vote_form'] = vote_form
        #     ctx['vote_url'] = 
        print('Not chached') #This is used to check cashing
        return ctx

    

class AlbumVoteCreateView(CreateView):
    form_class = AlbumVoteForm
    model = AlbumVote


    def form_valid(self, form):
        like = form.cleaned_data.get('like')
        user = self.request.user
        album_obj = Album.objects.get(pk=self.kwargs['song_id'])
        vote_obj, created = AlbumVote.objects.get_or_create(album = album_obj, user = user, like=like) 
        form.instance = vote_obj
        return super().form_valid(form)






class AlbumDetailView(DetailView):
    model = Album


class AlbumCreatView(CreateView):
    form_class = AlbumForm
    template_name = 'album/album_create.html'
    success_url = '/album/'


class AlbumDeleteView(DeleteView):
    model = Album
    success_url = reverse_lazy('music:album_list')


class AlbumUpdateView(UpdateView):
    model = Album
    form_class =AlbumForm #we can use form_class method or bellow fields method to declare the form
    # fields = ['title','discription','formate','singer']
    template_name_suffix = '_update_form'
    success_url = '/album/'