from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('auth/signup/', views.signup_view, name='signup'),
    path('auth/login/', views.login_view, name='login'),
    path('dashboard/student/', views.stdashboard, name='stdashboard'),
    path('dashboard/coach/', views.coachdashboard, name='coachdashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('make-booking/', views.bookings, name='bookings'),
    path("get-coaches/", views.get_coaches, name="get_coaches"),
    path("coach_sports/", views.coach_sports, name="coach_sports"),
    path("manage-booking/<int:id>", views.manage_booking, name="manage_booking")
]