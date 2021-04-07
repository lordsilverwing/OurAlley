from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import uuid
import boto3
from .models import Dog, Playdate, Profile, Photo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm
from django.conf import settings
import requests
from math import radians, cos, sin, asin, sqrt


# Haversine equation to caluculate distance between 2 points
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles
    return c * r

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
      # Send new user to profile update for their address and bio
      return redirect('profile_update', request.user.profile.id)
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

class ProfileUpdate(UpdateView):
  model = Profile
  fields = ['address', 'city', 'state', 'zipcode', 'bio']
  success_url = '/accounts/profile/'

  # convert the user's address into latitude and longitude
  def form_valid(self, form):
    position = form.instance.address.replace(' ', '+')
    position += '+' + form.instance.city + '+' + form.instance.state
    form.instance.longitude, form.instance.latitude = extract_lat_long_via_address(position)
    return super().form_valid(form)

class CreateDog(LoginRequiredMixin, CreateView):
  model = Dog
  fields = ['name', 'breed', 'size', 'age', 'description']
  success_url = '/accounts/profile/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class DogUpdate(UpdateView):
  model = Dog
  fields = ['breed', 'description', 'age', 'size']
  

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'

def playdate_detail(request, playdate_id):
  playdate = Playdate.objects.get(id=playdate_id)
  address = playdate.location.replace(' ', '+')
  local_dogs = Dog.objects.filter(playdate=playdate)
  return render(request, 'playdates/detail.html', {'playdate': playdate, 'local_dogs': local_dogs, 'address': address, 'api_key': settings.GOOGLE_MAPS_API_KEY})

def invite_index(request, playdate_id):
  playdate = Playdate.objects.get(id=playdate_id)
  long1 = request.user.profile.longitude
  lat1 = request.user.profile.latitude
  local_dogs = []
  other_dogs = Dog.objects.exclude(user=request.user)
  for dog in other_dogs:
    # compare the haversine equation of each dog's position to 1 mile
    if haversine(long1, lat1, dog.user.profile.longitude, dog.user.profile.latitude) < 1:
      local_dogs.append(dog)
  return render(request, 'playdates/invites.html', {'playdate_id': playdate.id, 'local_dogs': local_dogs})

def add_invites(request, playdate_id):
  playdate = Playdate.objects.get(id=playdate_id)
  # Add user's dog to playdate first
  for dog in playdate.user.dog_set.all():
    dog.playdate_set.add(playdate)
  # Add all the invited dogs to playdate
  for item in request.POST:
    if request.POST[item].isdigit():
      dog = Dog.objects.get(id=int(request.POST[item]))
      dog.playdate_set.add(playdate)
  return redirect('playdate', playdate_id)

def playdates_index(request):
  # these are the playdates the user made
  playdates = Playdate.objects.filter(user=request.user)
  # these ate the playdates the user's dogs were invited to
  invites = []
  dogs = Dog.objects.filter(user=request.user)
  for dog in dogs:
    # Get EVERY playdate that user's dogs are invited to
    [invites.append(playdate) for playdate in dog.playdate_set.all() if playdate not in invites]
    #  Remove the playdates the the user made
    [invites.remove(playdate) for playdate in invites if playdate in playdates]
  return render(request, 'playdates/index.html', {'playdates': playdates, 'invites': invites})

def add_invite(request):
  invites = Invite.objects.all()
  return render(request, '')

class CreatePlaydate(LoginRequiredMixin, CreateView):
  model = Playdate
  fields = ['time', 'date', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  return render(request, 'dogs/detail.html', { 'dog': dog })

@login_required
def add_photo(request, dog_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, settings.BUCKET, key)
            # build the full url string
            url = f"{settings.S3_BASE_URL}{settings.BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, dog_id=dog_id)
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', dog_id=dog_id)