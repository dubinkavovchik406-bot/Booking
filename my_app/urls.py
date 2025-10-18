from django.urls import path
from my_app import views
urlpatterns = [
    path("", views.home_page, name="home-page"),
    path("rooms-list/", views.rooms_list, name = "rooms-list"),
    path("room-detail/<int:r_id>/", views.room_detail, name = "room-detail"),
]