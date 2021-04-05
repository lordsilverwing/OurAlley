from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dogs/', views.dogs_index, name='index'),
    path('dogs/create', views.CreateDog.as_view(), name='add_dog'),
    path('dogs/<int:dog_id>/add_invite/', views.add_invite, name='add_invite'),
    #path('dogs/<int:dog_id>/add_photo/', views.add_photo, name='add_photo'),
    path('playdates/', views.playdates_index, name='play_index'),
    path('dogs/<int:dog_id>/', views.dogs_detail, name='detail'),
]