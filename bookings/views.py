from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from core.forms import ReviewForm
from core.models import Review

from .forms import BookingForm
from .models import Booking

RATING_RANGE = range(1, 6)


def booking_create(request):
    booking_form = BookingForm()
    review_form = ReviewForm()
    if request.method == "POST":
        form_name = request.POST.get("form_name")
        if form_name == "booking":
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save()
                messages.success(request, "Booking confirmed! Our concierge will be in touch shortly.")
                return redirect("bookings:booking_confirmation", reference=booking.booking_reference)
        elif form_name == "review":
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review_form.save()
                messages.success(request, "Thank you for sharing your experience with HotelEase.")
                return redirect(f"{reverse('bookings:booking_form')}#guest-reviews")

    reviews = Review.objects.order_by("-created_at")
    rate_cards = [
        {
            "code": value,
            "label": label,
            "price": Booking.ROOM_TYPE_RATES.get(value, 0),
        }
        for value, label in Booking.ROOM_TYPE_CHOICES
    ]
    context = {
        "form": booking_form,
        "review_form": review_form,
        "reviews": reviews,
        "rating_range": RATING_RANGE,
        "rate_map": Booking.ROOM_TYPE_RATES,
        "rate_cards": rate_cards,
        "airport_charge": Booking.AIRPORT_CHARGE,
    }
    return render(request, "bookings/booking_form.html", context)


def booking_confirmation(request, reference):
    booking = get_object_or_404(Booking.objects.select_related("room"), booking_reference=reference)
    context = {
        "booking": booking,
        "rate_map": Booking.ROOM_TYPE_RATES,
        "airport_charge": Booking.AIRPORT_CHARGE,
    }
    return render(request, "bookings/booking_confirmation.html", context)
