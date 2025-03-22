from django.core.management.base import BaseCommand
from main.models import Booking
from main.utils import send_booking_notification

class Command(BaseCommand):
    help = 'Sends booking notifications to coaches and students for new bookings.'

    def handle(self, *args, **kwargs):
        # Get all bookings where email_sent is False
        bookings = Booking.objects.filter(email_sent=False)

        for booking in bookings:
            try:
                # Send the notification email
                send_booking_notification(booking)
                self.stdout.write(self.style.SUCCESS(f"Notification sent for booking: {booking}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to send notification for booking {booking}: {e}"))

        self.stdout.write(self.style.SUCCESS("All booking notifications sent successfully."))