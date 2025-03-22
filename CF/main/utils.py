from django.core.mail import send_mail
from django.conf import settings
from main.models import Booking

def send_booking_notification(booking):
    """
    Sends an email notification to the coach and student about the booking.
    """
    # Email subject
    subject = f"New Booking Notification: {booking.coach.first_name} and {booking.student.first_name}"

    # Email message for the coach
    coach_message = (
        f"Dear {booking.coach.first_name},\n\n"
        f"You have a new booking with {booking.student.first_name} on {booking.session}.\n\n"
        f"Thank you,\n"
        f"Your Booking System"
    )

    # Email message for the student
    student_message = (
        f"Dear {booking.student.first_name},\n\n"
        f"Your booking with {booking.coach.first_name} on {booking.session} has been confirmed.\n\n"
        f"Thank you,\n"
        f"Your Booking System"
    )

    # Send email to the coach
    send_mail(
        subject,
        coach_message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.coach.email],  # Use the coach's email field
        fail_silently=False,
    )

    # Send email to the student
    send_mail(
        subject,
        student_message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.student.email],  # Use the student's email field
        fail_silently=False,
    )

    # Mark the email as sent
    booking.email_sent = True
    booking.save()