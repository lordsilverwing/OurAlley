from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dogs/', views.dogs_index, name='index'),
    path('dogs/create', views.CreateDog.as_view(), name='add_dog'),
    path('dogs/<int:pk>/update/', views.DogUpdate.as_view(), name='dogs_update'),
    path('dogs/<int:pk>/delete/', views.DogDelete.as_view(), name='dogs_delete'),
    path('dogs/<int:dog_id>/add_invite/', views.add_invite, name='add_invite'),
    #path('dogs/<int:dog_id>/add_photo/', views.add_photo, name='add_photo'),
    path('playdates/', views.playdates_index, name='play_index'),
    path('playdates/create', views.CreatePlaydate.as_view(), name='add_playdate'),
    path('playdates/<int:playdate_id>/', views.playdate_detail, name='playdate'),
    path('dogs/<int:dog_id>/', views.dogs_detail, name='detail'),
]