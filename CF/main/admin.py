from django.contrib import admin

# Register your models here.
from .models import Student, Review, Coach, Sport, Booking
CoachFinder = [Student, Review, Coach, Sport, Booking]
admin.site.register(CoachFinder)