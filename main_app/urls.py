from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/signup/', views.signup, name='signup'),
    path('dogs/', views.dogs_index, name='index'),
    path('dogs/create', views.CreateDog.as_view(), name='add_dog'),
]