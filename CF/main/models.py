from django.db import models
from django.contrib.auth.models import User

# Student Model
class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    sport = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(User, related_name="student", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Review Model
class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_reviews")
    # Removed max_length from IntegerField
    rating = models.IntegerField()
    comment = models.TextField(max_length=100)
    review_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.student.first_name}"

# Coach Model
class Coach(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    sport = models.CharField(max_length=30, null=True, blank=True)
    # Changed capitalization to match Python naming conventions
    experience = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, related_name="coach", on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Sport Model
class Sport(models.Model):
    sport_name = models.CharField(max_length=30)
    coach = models.ManyToManyField(Coach, related_name="coached_sports", blank=True)
    student = models.ManyToManyField(Student,  related_name="student_sports", blank=True)
    
    def __str__(self):
        return self.sport_name

# Booking Model
class Booking(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name="bookings", default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="bookings", null=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name="booked_sessions", null=True)
    # Removed max_length from DateTimeField (not applicable)
    session = models.DateTimeField()
    status = models.CharField(max_length=100)
    email_sent = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Booking {self.student.first_name} with {self.coach.first_name}"