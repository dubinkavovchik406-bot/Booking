from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from my_app.models import Room, Order

def home_page(request):
    context = {
        "render_string": _("This is home page")
    }

    return render(
        request=request, template_name="booking/home-page.html", context=context
    )


def rooms_list(request):
    rooms = Room.objects.all()

    today = timezone.now().date()

    rooms_data = []
    for room in rooms:
        is_booked = Order.objects.filter(
            room=room,
            start_time__lte=today,
            end_time__gte=today
        ).exists()

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
        "room": room,
        "room_id_for_url": r_id,
    }

    return render(
        request=request, template_name="booking/room-detail.html", context=context
    )

@login_required
def order_form(request, r_id):
    error_message = None

    room = get_object_or_404(Room, id=r_id)

    if request.method == "POST":
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        today = timezone.now().date().isoformat()

        if not start_time or not end_time:
            error_message = _("Please select a start date and end date!")

        elif start_time < today:
            error_message = _("The start date cannot be in the past!")

        elif start_time >= end_time:
            error_message = _("The end date cannot be earlier than or equal to the start date!")

        if not error_message:
            conflicting_orders = Order.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if conflicting_orders:
                error_message = _("The selected period is not available. It overlaps with an existing reservation.")

        if not error_message:
            try:
                order = Order.objects.create(
                    user=request.user,
                    room=room,
                    start_time=start_time,
                    end_time=end_time
                )
                return redirect("order-form-details", pk=order.id)

            except ValidationError:
                error_message = _("Wrong value for time!")

        context = {
            "room_id": r_id,
            "room": room,
            "error_message": error_message,
            "start_time": start_time,
            "end_time": end_time,
        }
    else:
        context = {
            "room_id": r_id,
            "room": room,
        }
    return render(request=request, template_name="booking/order-form.html", context=context)

@login_required
def order_form_details(request, pk):
    order = get_object_or_404(Order, id=pk)

    context = {
        "order": order
    }

    return render(request=request, template_name="booking/order-form-details.html", context=context)