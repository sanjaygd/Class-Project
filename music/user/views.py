from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView,DetailView,View

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from user.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

from django.http import JsonResponse

from .forms import SignUpForm,ProfileImageForm,ProfileForm
from .models import ProfileImage,Profile


from .serializers import UserSerializer
from rest_framework import viewsets


User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileEditView(View):
    profile_class = ProfileForm
    profile_image_class = ProfileImageForm
    template_name = 'user/profile_edit.html'

    def get(self,request,pk):
        if pk:
            user = User.objects.get(pk=pk)
            profile = Profile.objects.get(user = user)
            profile_image = ProfileImage.objects.get(user = user)
            profile_form = self.profile_class(instance = profile)
            profile_image_form = self.profile_image_class(instance = profile_image)
            
            context = {
            'profile_form':profile_form,
            'profile_image_form':profile_image_form
                }
            return render(request, self.template_name, context)

        else:
            profile_form = self.profile_class(None)
            profile_image_form = self.profile_image_class(None)
            context = {
                'profile_form':profile_form,
                'profile_image_form':profile_image_form
                }
            return render(request, self.template_name, context)


    def post(self,request,pk=None, **kwargs):

        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user = user)
        profile_image = ProfileImage.objects.get(user = user)
        profile_form = self.profile_class(request.POST,instance=profile)
        profile_image_form = self.profile_image_class(request.POST, request.FILES, instance=profile_image)

        if user == request.user:
            if profile_image_form.is_valid() and profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile_image = profile_image_form.save(commit=False)

                profile.user = self.request.user
                profile_image.user = self.request.user

                profile.save()
                profile_image.save()

                return redirect('music:album_list')

        context = {
                'profile_form':profile_form,
                'profile_image_form':profile_image_form,
                'error_message':"You could not able to edit other user's profile",
                }
        return render(request, self.template_name, context)
        



# class ProfileEditView(UpdateView):
#     model = ProfileImage
#     template_name = 'user/profile_edit.html'
#     form_class = ProfileImageForm
#     success_url = '/album/'

#     # We can use above form_class or below image_form to render form to user_profile template
#     def get_context_data(self,**kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx['profile_form'] = self.profile_form
#         return ctx

#     def get_object(self,queryset=None):
#         profile = super().get_object(queryset)
#         user = self.request.user
#         if profile.user != user:
#             raise PermissionDenied('You can not edit other user profile')
#         return profile


#     def profile_form(self):
#         if self.request.user.is_authenticated:
#             return ProfileForm()
#         return None




class ProfileAddView(CreateView):
    model = ProfileImage
    form_class = ProfileImageForm
    template_name = 'user/user_profile.html'


    # def get_context_data(self,**kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     ctx['user'] = self.request.user
    #     return ctx

class ProfileDetailView(DetailView):
    model = User
    template_name = 'user/profile_detail.html'





def validate_username(request):
    username = request.GET.get('username',None)
    data = {
        'is_taken':User.objects.filter(username__iexact = username).exists()
    }

    if data['is_taken']:
        data['error_message'] = "A user with this username is already exists please change the username"
    return JsonResponse(data)


class LoginFormView(LoginView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['rend'] = 'This is for test'
        return ctx



# #We can use class based signup when we using allauth authentication

# class RegisterView(CreateView):
#     template_name = 'user/register.html'
#     form_class = SinupForm
#     success_url = reverse_lazy('music:album_list')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            test = render_to_string('user/test.html')
            print('test_1')
            message = render_to_string('user/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message,test)
            return redirect('user:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'user/register.html', {'form': form})



def account_activation_sent(request):
    return render(request, 'user/account_activation_sent.html')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('user:signup_done')
    else:
        return render(request, 'user/account_activation_invalid.html')



def signup_done(request):
    return render(request, 'user/signup_done.html')





    
    