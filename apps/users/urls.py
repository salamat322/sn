from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LogoutView, LoginView

from . import views


urlpatterns = [
    path('', views.signup, name='signup'),
    path('<int:pk>/profile/', views.profile, name='profile'),
    path('users/', views.users_page, name='users'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page="main_page"), name="logout"),
    path('follow/<int:pk>', views.follow_user, name='follow'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]