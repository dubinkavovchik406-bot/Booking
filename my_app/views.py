from django.shortcuts import render
from my_app.models import Customer, Room, Order
# Create your views here.

def home_page(request):
    context = {
        "render_string": "This is home page. Hello!!"
    }

    return render(
        request=request, template_name="booking/home-page.html", context=context
    )

def rooms_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms
    }

    return render(
        request=request, template_name="booking/rooms-list.html", context=context
    )
