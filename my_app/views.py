from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404

from my_app.models import Customer, Room, Order

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

def room_detail(request, r_id):
    room = Room.objects.get(id=r_id)
    context = {
        "room": room
    }

    return render(
        request=request, template_name="booking/room-detail.html", context=context
    )

def order_form(request, r_id):
    if request.method == "POST":
        customer_id = request.POST.get("customer-id")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            customer = get_object_or_404(Customer, id=customer_id)
            room = get_object_or_404(Room, id=r_id)
        except ValueError:
            return HttpResponse(
                "Wrong value for customer id or room number!",
                status=400
            )
        except Http404:
            return HttpResponse(
                "Customer or room not found",
                status=404
            )

        order = Order.objects.create(
            customer=customer,
            room=room,
            start_time=start_time,
            end_time=end_time
        )
        return redirect("order-form-details", pk=order.id)
    else:
        context = {
            'room_id': r_id
        }
        return render(request=request, template_name="booking/order-form.html", context=context)

def order_form_details(request, pk):
    try:
        order = get_object_or_404(Order, id=pk)
        context = {
            "order": order
        }
        return render(request=request, template_name="booking/order-form-details.html", context=context)
    except Http404:
        return HttpResponse(
            "This order not found",
            status=404
        )