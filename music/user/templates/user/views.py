from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from user.tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text


from .forms import SinupForm

User = get_user_model()



def signup(request):
    if request.method == 'POST':
        form = SinupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('user/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SinupForm()
    return render(request, 'user/register.html', {'form': form})



def account_activation_sent(request):
    return render(request, '')



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
        return redirect('home')
    else:
        return render(request, 'user/account_activation_invalid.html')







# class RegisterView(CreateView):
#     template_name = 'user/register.html'
#     form_class = SinupForm
#     success_url = reverse_lazy('music:album_list')

    
    