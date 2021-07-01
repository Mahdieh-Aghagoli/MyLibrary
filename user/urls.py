from django.contrib.auth import views as v
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('login/', v.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(), name='logout'),

    re_path(r'send-email/(?P<user_slug>[-\w]+)/', SendEmailVCode.as_view(), name='send-email'),
    path('emailVerify/<uidb64>/<token>/', EmailVerify.as_view(), name='emailVerify'),

    re_path(r'edit_profile/(?P<slug>[-\w]+)/', ProfileView.as_view(), name='edit_profile'),
]
