from django.conf.urls import url

from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('register', user_views.register, name='register'),
    url('profile', user_views.profile, name='profile'),
    url('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

