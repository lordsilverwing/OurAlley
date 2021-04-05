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
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=20, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
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
    time = models.TimeField('time to play')
    date = models.DateField('date of play')
    description = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
        return f"Photo for cat_id: {self.dog_id} @{self.url}"