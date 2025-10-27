from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    today = timezone.now().date()

    rooms_data = []
    for room in rooms:
        is_booked = Order.objects.filter(room=room,end_time__gte=today).exists()

        rooms_data.append({
            'room': room,
            'is_booked': is_booked
        })

    context = {
        "rooms_data": rooms_data
    }

    return render(
        request=request, template_name="booking/rooms-list.html", context=context
    )

def room_detail(request, r_id):
    room = get_object_or_404(Room, id=r_id)
    context = {
        "room": room
    }

    return render(
        request=request, template_name="booking/room-detail.html", context=context
    )

def order_form(request, r_id):
    error_message = None
    customer = None

    room = get_object_or_404(Room, id=r_id)

    if request.method == "POST":
        customer_email = request.POST.get("customer-email")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            customer = Customer.objects.get(email__iexact=customer_email)

        except Customer.DoesNotExist:
            error_message = "Customer email Doesn't exist"
        except ValueError:
            error_message = "Wrong value for customer email!"

        if customer and not error_message:
            if not start_time or not end_time:
                error_message = "Пожалуйста, выберите дату начала и дату окончания."

            elif start_time >= end_time:
                error_message = "Дата окончания не может быть раньше или равна дате начала."

            if not error_message:
                conflicting_orders = Order.objects.filter(
                    room=room,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()

                if conflicting_orders:
                    error_message = "Выбранный период недоступен. Он пересекается с существующей бронью."

            if not error_message:
                try:
                    order = Order.objects.create(
                        customer=customer,
                        room=room,
                        start_time=start_time,
                        end_time=end_time
                    )
                    return redirect("order-form-details", pk=order.id)

                except ValidationError:
                    error_message = "Wrong value for time!"

        context = {
            'room_id': r_id,
            'error_message': error_message,
            'customer_email': customer_email,
            'start_time': start_time,
            'end_time': end_time,
        }
        return render(request=request, template_name="booking/order-form.html", context=context)

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