from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .import utils
from main.models import Student, Coach, Sport,Booking  # Ensure models are imported
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime

# Index View
def index_view(request):
    return render(request, 'index.html', {})

# Login View
@csrf_exempt
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html", {})
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return JsonResponse({"error": "Email and password are required"}, status=400)

            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                
                if Student.objects.filter(user=user).exists():
                    response_data = {
                        "message": "Login successful",
                        "redirect_url": "/dashboard/student/",
                        "user": {
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "user_type": "student"
                        }
                    }
                elif Coach.objects.filter(user=user).exists():
                    response_data = {
                        "message": "Login successful",
                        "redirect_url": "/dashboard/coach/",
                        "user": {
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "user_type": "coach"
                        }
                    }
                else:
                    return JsonResponse({"error": "User type not recognized"}, status=400)
                
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "Invalid email or password"}, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

# Signup View
@csrf_exempt
def signup_view(request):
    if request.method == "GET":
        return render(request, 'signup.html', {})

    elif request.method == "POST":
        try:
            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "").strip()
            confirm_password = request.POST.get("confirmPassword", "").strip()
            firstname = request.POST.get("first_name", "").strip()
            lastname = request.POST.get("last_name", "").strip()
            user_type = request.POST.get("userType", "").strip().lower()

            if not all([email, password, firstname, lastname, user_type]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if password != confirm_password:
                return JsonResponse({"error": "Passwords do not match"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "User with this email already exists"}, status=400)

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname
            )

            if user_type == "athlete":
                Student.objects.create(user=user, email=email, first_name=firstname, last_name=lastname)
                dashboard_url = "/dashboard/student/"

            elif user_type == "coach":
                Coach.objects.create(
                    user=user,
                    email=email,
                    first_name=firstname,
                    last_name=lastname,
                    gender=request.POST.get("gender") or None,
                    sport=request.POST.get("sport") or None,
                    experience=request.POST.get("experience") or None
                )
                dashboard_url = "/dashboard/coach/"

            else:
                user.delete()  # Delete the user if user_type is invalid
                return JsonResponse({"error": "Invalid user type"}, status=400)

            return JsonResponse(
                {
                    "message": "User created successfully!",
                    "redirect_url": dashboard_url,
                    "user": {
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "user_type": user_type,
                    },
                },
                status=201
            )

        except Exception as e:
            return JsonResponse({"error": f"Something went wrong: {str(e)}"}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# Dashboard Views
@login_required(login_url="/auth/login")
def stdashboard(request):
    user = request.user
    if not hasattr(user, 'student'):
        return HttpResponseForbidden("You are not authorized to view this")
    
    if request.method != "GET":
        return JsonResponse({
            "message": "Method not allowed",
            "status": 405
        }, status=405)
    student = user.student
    booking_list = []
    try:
        bookings = Booking.objects.select_related("coach", "sport").filter(student=student, status="approved")
        booking_list = [
            {
                "id": booking.id,
                "sport": booking.sport.sport_name,
                "coach": f"{booking.coach.first_name} {booking.coach.last_name}",
                "session": booking.session,
                "status": booking.status
            } for booking in bookings
        ] if bookings else []
    except Exception as e:
        print(f"Error: {str(e)}")

    return render(request, 'stdashboard.html', {"bookings": booking_list, "user": user})

@login_required(login_url="/auth/login")
def coachdashboard(request):
    user = request.user
    if not hasattr(user, 'coach'):
        return HttpResponseForbidden("You are not authorized to view this page")
    booking_list= []
    coach = user.coach
    if coach:
        status = ["pending", "approved"]
        all_bookings = Booking.objects.select_related("coach", "sport").filter(coach=coach)
        bookings = all_bookings.filter(status__in=status)   
        booking_list = [
            {
                "id": booking.id,
                "sport": booking.sport.sport_name,
                "student": f"{booking.student.user.first_name} {booking.student.user.last_name}",
                "session": booking.session,
                "status": booking.status
            } for booking in bookings
        ] if bookings else  []


    return render(request, 'coachdashboard.html', {"bookings": booking_list, "user": user, "stats": {
        "bookings_count": bookings.count(),
        "pending_count": all_bookings.filter(status="pending").count(),
        "approved_count": all_bookings.filter(status="approved").count(),
        "declined_count": all_bookings.filter(status="declined").count()
    }})

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        user_type = request.POST['userType']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken')
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
                user.profile.user_type = user_type  # Assuming you have a profile model with user_type field
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('main:login')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'signup.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        if hasattr(user, 'profile'):
            user.profile.gender = request.POST.get('gender', user.profile.gender)
            user.profile.sport = request.POST.get('sport', user.profile.sport)
            user.profile.experience = request.POST.get('experience', user.profile.experience)
            user.profile.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('main:stdashboard' if hasattr(user, 'student') else 'main:coachdashboard')

    return render(request, 'stdashboard.html' if hasattr(request.user, 'student') else 'coachdashboard.html')

@login_required
def bookings(request):
    user = request.user
    if request.method == 'GET':
        
        return render(request, 'stdashboard.html', {})

    elif request.method == 'POST':
        try:

            # Get Student instance from User
            sport_id = request.POST.get('sport',None)
            coach_id = request.POST.get('coach',None)
            date = request.POST.get('date',None)
            time = request.POST.get('time',None)

            if not(sport_id and coach_id and date and time):
                return JsonResponse({"error": "All fields are required"}, status=400)

            student = Student.objects.filter(user=user).first()
            sport = Sport.objects.filter(id=sport_id).first()
            coach = Coach.objects.filter(id=coach_id).first()
            
            if not sport:
                print("Sport not found")
                return JsonResponse({"error": "Sport not found"}, status=404)
            
            if not coach:
                print("Coach not found")
                return JsonResponse({"error": "Coach not found"}, status=404)
            
            if not student:
                print("Student not found")
                return JsonResponse({"error": "Student not found"}, status=404)
            
            session_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

            new_booking = Booking.objects.create(
                sport=sport,
                student=student,
                coach=coach,
                session=session_datetime,
                status="pending"
                
            )
            new_booking.save()

            return JsonResponse({"message": "Booking created successfully!"}, status=200)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        
@login_required
def get_coaches(request):
    sport_id = request.GET.get('sport_id')
    if not sport_id:
        return JsonResponse({"error": "Sport ID is required"}, status=400)

    try:
        sport = Sport.objects.get(id=sport_id)
        coaches = Coach.objects.filter(sport=sport.sport_name)
        coach_list = [{"id": c.id, "first_name": c.first_name, "last_name": c.last_name} for c in coaches]

        return JsonResponse({"coaches": coach_list}, status=200)
    except Sport.DoesNotExist:
        return JsonResponse({"error": "Sport not found"}, status=404)
    
def coach_sports(request):
    user = request.user
    if request.method != "GET":
        return JsonResponse({
            "message": "Method not allowed",
            "status": 405
        }, status=405)
    
    try:
        sport_qs = Sport.objects.all()

        sports = [
            {
                "name": sport.sport_name,
                "id": sport.id,
                "coaches": [
                    {
                        "id": coach.id,
                        "name": f"{coach.first_name} {coach.last_name}",
                    } for coach in sport.coach.all()
                ]
            } for sport in sport_qs 
        ] if sport_qs else []

        print(f"Sports: {sports}")
        return JsonResponse({"sports": sports}, status=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"sports": []}, status=500)

@login_required(login_url="/auth/login")
def manage_booking(request, id):
    user = request.user
    
    if not hasattr(user, 'coach'):
        return HttpResponseForbidden("You are not authorized to view this page")
    
    coach = user.coach
    
    if id is None:
        return JsonResponse({
            "message": "Booking ID is required",
            "status": 400
        }, status=400)
    
    if request.method != 'POST':
        return JsonResponse({
            "message": "Method not allowed",
            "status": 405
        }, status=405)
    try:
        booking = Booking.objects.get(id=id)
        booked_coach = booking.coach
        if booked_coach != coach:
            return HttpResponseForbidden("You are not authorized to view this page")
        
        action = request.POST.get('action', None)
        if not action:
            return JsonResponse({
                "message": "I dont know what to do",
                "status": 400
            }, status=400)
        if action == "approve" or action == "decline":
            booking.status = action+"d"
            if action == "approve":
                email_sent=False
                # utils.send_booking_confirmation_email(booking.id)
            booking.save()
        elif action == "delete":
            booking.delete()
        else:
            return JsonResponse({
                "message": "Invalid action",
                "status": 400
            }, status=400)
        
        return JsonResponse({
            "message": "Booking updated successfully",
            "status": 200
        },status=200)
    
    except Booking.DoesNotExist:
        return JsonResponse({
            "message": "Missing data",
            "status": 404
        }, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
