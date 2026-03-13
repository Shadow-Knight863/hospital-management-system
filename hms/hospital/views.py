from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Availability
import requests


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
        slot.save()

        # Call serverless email function
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

    return redirect("/")


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