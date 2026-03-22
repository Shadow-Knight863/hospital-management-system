from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Availability, Doctor, Patient, Booking
import requests
import urllib.parse


# Home page – show all available slots
@login_required
def home(request):
    slots = Availability.objects.all()
    return render(request, "slots.html", {"slots": slots})


# Booking function
@login_required
def book_slot(request, slot_id):
    slot = Availability.objects.get(id=slot_id)

    if not slot.is_booked:
        slot.is_booked = True
        slot.booked_by = request.user
        slot.save()

        # Create Patient if not exists
        patient, created = Patient.objects.get_or_create(user=request.user)

        # Create Booking entry
        Booking.objects.create(
            doctor=slot.doctor,
            patient=patient,
            slot=slot
        )

        # Serverless email
        try:
            requests.post(
                "http://localhost:3000/dev/send-email",
                json={
                    "email": request.user.email,
                    "action": "BOOKING_CONFIRMATION"
                }
            )
        except:
            print("Serverless email service not running")

        messages.success(request, "Appointment booked successfully!")

        # ✅ Redirect to calendar page (NEW)
        return redirect(f"/add-to-calendar/{slot.id}/")

    return redirect("/")


# ✅ Add to Calendar Page (NEW FUNCTION)
@login_required
def add_to_calendar(request, slot_id):
    slot = Availability.objects.get(id=slot_id)

    doctor_name = slot.doctor.user.username
    patient_name = request.user.username

    event_title = f"Appointment with Dr. {doctor_name}"
    event_details = f"Patient: {patient_name}"

    start = f"{slot.date}T{slot.start_time}"
    end = f"{slot.date}T{slot.end_time}"

    calendar_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    calendar_url += "&text=" + urllib.parse.quote(event_title)
    calendar_url += "&details=" + urllib.parse.quote(event_details)
    calendar_url += "&dates=" + start.replace(":", "").replace("-", "") + "/" + end.replace(":", "").replace("-", "")

    return render(request, "add_to_calendar.html", {
        "calendar_url": calendar_url
    })


# Registration page
def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("/")

    return render(request, "register.html")


# Doctor Dashboard
@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return redirect("/")

    doctor = request.user.doctor
    slots = Availability.objects.filter(doctor=doctor)

    return render(request, 'doctor_dashboard.html', {'slots': slots})


# Add Slot
@login_required
def add_slot(request):
    if not hasattr(request.user, 'doctor'):
        return redirect("/")

    if request.method == "POST":
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        Availability.objects.create(
            doctor=request.user.doctor,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

    return redirect("/doctor-dashboard/")


# Delete Slot
@login_required
def delete_slot(request, slot_id):
    slot = Availability.objects.get(id=slot_id)

    if slot.doctor.user == request.user:
        slot.delete()

    return redirect("/doctor-dashboard/")