from django import forms

from core.forms import StyledFormMixin
from core.models import Room

from .models import Booking


class BookingForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Booking
        fields = (
            "full_name",
            "cnic",
            "address",
            "room_type",
            "booking_days",
            "airport_pick_drop",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Guest full name"}),
            "cnic": forms.TextInput(attrs={"placeholder": "13-digit CNIC"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Residential address"}),
            "booking_days": forms.NumberInput(attrs={"min": 1, "max": 7, "value": 1}),
        }
        labels = {
            "cnic": "CNIC",
            "airport_pick_drop": "Add Airport Pick & Drop (Rs. 7,000)",
        }

    def clean_room_type(self):
        room_type = self.cleaned_data.get("room_type")
        if room_type and not Room.objects.filter(room_type=room_type).exists():
            raise forms.ValidationError("This room type is currently unavailable. Please choose another category or contact concierge.")
        return room_type

    def clean_booking_days(self):
        days = self.cleaned_data.get("booking_days")
        if days and not 1 <= days <= 7:
            raise forms.ValidationError("Bookings can be made for 1 to 7 days.")
        return days
