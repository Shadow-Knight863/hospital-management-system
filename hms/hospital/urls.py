from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("book/<int:slot_id>/", views.book_slot, name="book_slot"),

    path("register/", views.register, name="register"),

    path("add-to-calendar/<int:slot_id>/", views.add_to_calendar, name="add_to_calendar"),

    # ✅ Doctor Dashboard
    path("doctor-dashboard/", views.doctor_dashboard, name="doctor_dashboard"),

    # ✅ Add Slot
    path("add-slot/", views.add_slot, name="add_slot"),

    # ✅ Delete Slot
    path("delete-slot/<int:slot_id>/", views.delete_slot, name="delete_slot"),
]