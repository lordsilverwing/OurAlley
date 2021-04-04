from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Dog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from django.conf import settings

# Create your views here.
def home(request):
  context = {
    'api_key': settings.GOOGLE_MAPS_API_KEY
  }
  return render(request, 'home.html', context)

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request):
  return render(request, 'profile.html')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('profile')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', { 'dogs': dogs })