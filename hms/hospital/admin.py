from django.contrib import admin
from .models import Doctor, Patient, Availability, Booking

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Availability)
admin.site.register(Booking)