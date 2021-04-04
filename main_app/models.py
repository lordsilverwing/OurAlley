from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

DOGSIZE = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('G', 'Giant')
)

# Create your models here.
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
