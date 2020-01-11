from django.contrib import admin
from django.urls import path,include
# from .views import  RegisterView,
from django.contrib.auth import views as auth_view
from user import views as user_views
from django.conf import settings
from django.conf.urls.static import static




app_name = 'user'
urlpatterns = [
   
    
    # path('login/', auth_view.LoginView.as_view(),name='login'),
    path('login/', user_views.LoginFormView.as_view(),name='login'), 
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),

    path('account/signup/', user_views.signup,name='sinup'),
    path('account/ajax/validate_username/', user_views.validate_username, name='validate_username'),
    path('account/account_activation_sent/', user_views.account_activation_sent, name='account_activation_sent'),
    path('account/activate/<uidb64>/<token>/', user_views.activate, name='activate'),
    path('account/signup_done/', user_views.signup_done, name='signup_done'),

    path('password_reset/',auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done',auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/<int:pk>/',user_views.ProfileEditView.as_view(), name='edit_profile'),
    path('add_profile/<int:pk>/',user_views.ProfileAddView.as_view(), name='add_profile'),
    path('detail_profile/<int:pk>/',user_views.ProfileDetailView.as_view(), name='detail_profile'),

]







'''
need to install crispy form for better look using pip3 install django-crispy-forms,
and add the app in installed app like bellow

INSTALLED_APPS = [
    ...

    'crispy_forms',
]

and add the tag in settings.py as bellow

CRISPY_TEMPLATE_PACK = 'bootstrap4'

refer /home/sanjay/Hacker make/CRUD mixins/Bootstrap 4 Forms With Django for more info.
'''
    
    

