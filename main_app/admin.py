from django.contrib import admin

from .models import Dog, Playdate, Invite

# Register your models here
admin.site.register(Dog)
admin.site.register(Playdate)
admin.site.register(Invite)