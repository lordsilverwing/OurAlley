from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Dog, Playdate, Invite, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from django.conf import settings
import requests


# Helper function to convert an address to longitude and latitude
def extract_lat_long_via_address(address_or_zipcode):
  lat, lng = None, None
  # build up the url for the request
  api_key = settings.GOOGLE_GEOCODE_API_KEY
  base_url = "https://maps.googleapis.com/maps/api/geocode/json"
  endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
  api_response = requests.get(endpoint)
  response_dict = api_response.json()
  # successfully got the json, so get the lat and long
  if response_dict['status'] == 'OK':
    lat = response_dict['results'][0]['geometry']['location']['lat']
    lng = response_dict['results'][0]['geometry']['location']['lng']
  return lat, lng

# Create your views here.
def home(request):
  # test code to show how to use geocode and embedded maps
  # lat, lng = extract_lat_long_via_address('345+Chelmsford+Drive+Brentwood+CA')
  context = {
    # 'api_key': settings.GOOGLE_MAPS_API_KEY,
    # 'lat': lat,
    # 'lng': lng
  }
  return render(request, 'home.html', context)

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request):
  profile = Profile.objects.all()
  return render(request, 'profile.html', { 'profile' : profile})

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

class CreateDog(LoginRequiredMixin, CreateView):
  model = Dog
  fields = ['name', 'breed', 'size', 'age', 'description']
  success_url = '/accounts/profile/'
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)


class DogUpdate(UpdateView):
  model = Dog
 
  fields = ['breed', 'description', 'age', 'size']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'

  

def playdates_index(request):
  playdates = Playdate.objects.all()
  return render(request, 'playdates/index.html', {'playdates': playdates})

def add_invite(request):
  invites = Invite.objects.all()
  return render(request, '')

class CreatePlaydate(LoginRequiredMixin, CreateView):
  model = Playdate
  fields = ['time', 'date', 'description']

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  return render(request, 'dogs/detail.html', { 'dog': dog })
