from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("book/<int:slot_id>/", views.book_slot, name="book_slot"),

    path("register/", views.register, name="register"),

]