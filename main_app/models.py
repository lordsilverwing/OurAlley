from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver

DOGSIZE = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('G', 'Giant')
)

RESPONSE = (
    (0, 'Decline'),
    (1, 'Accept'),
    (2, 'Tentative')
)

TIMES = (
    ('0', '6:00am'),
    ('1', '6:30am'),
    ('2', '7:00am'), 
    ('3', '7:30am'), 
    ('4', '8:00am'), 
    ('5', '8:30am'), 
    ('6', '9:00am'), 
    ('7', '9:30am'),
    ('8', '10:00am'),
    ('9', '10:30am'),
    ('10', '11:00am'), 
    ('11', '11:30am'), 
    ('12', '12:00pm'), 
    ('13', '12:30m'), 
    ('14', '1:00pm'), 
    ('15', '1:30pm'),
    ('16', '2:00pm'),
    ('17', '2:30pm'),
    ('18', '3:00pm'), 
    ('19', '3:30pm'), 
    ('20', '4:00pm'), 
    ('21', '4:30pm'), 
    ('22', '5:00pm'), 
    ('23', '5:30pm'),
    ('24', '6:00pm'), 
    ('25', '6:30pm'),
    ('26', '7:00pm'),
    ('27', '7:30pm'),
    ('28', '8:00pm'), 
    ('29', '8:30pm'), 
    ('30', '9:00pm'), 
    ('31', '9:30pm'), 
    ('32', '10:00pm')
)
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=300, default='Hello')
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Dog(models.Model):
    name = models.CharField(max_length=20)
    size = models.CharField(
        max_length=1,
        choices=DOGSIZE,
        default=DOGSIZE[0][0]
    )
    breed = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    age = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'dog_id': self.id})

class Playdate(models.Model):
    time = models.CharField(
        max_length=7,
        choices=TIMES,
        default=TIMES[14]
    )
    date = models.DateField('date of play')
    description = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default='Home')

    def get_absolute_url(self):
        return reverse('play_index')

class Invite(models.Model):
    response = models.IntegerField(
        choices=RESPONSE,
        default=RESPONSE[2][0]
    )
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    playdate = models.ForeignKey(Playdate, on_delete=models.CASCADE)

class Photo(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dog_id: {self.dog_id} @{self.url}"