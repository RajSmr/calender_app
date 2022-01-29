from django.contrib import admin
from .models import Venue, User, Event

# Adding our models
admin.site.register(Venue)
admin.site.register(User)
admin.site.register(Event)
