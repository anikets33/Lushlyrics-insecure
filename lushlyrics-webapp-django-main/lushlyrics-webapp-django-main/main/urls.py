from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path("signup/", views.user_signup, name='user_signup'),
    path("login/", views.user_login, name='user_login'),
    path("logout/", views.user_logout, name='user_logout'),
    path("recover/", views.recover_password, name='recover_password'),
    path('reset_password/<id>', views.reset_password, name='reset_password'),
]