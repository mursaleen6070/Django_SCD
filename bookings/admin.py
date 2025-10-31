from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = (
		"booking_reference",
		"full_name",
		"room_type",
		"booking_days",
		"airport_pick_drop",
		"total_price",
		"status",
		"created_at",
	)
	list_filter = ("room_type", "status", "airport_pick_drop")
	search_fields = ("booking_reference", "full_name", "email", "phone_number")
	readonly_fields = ("booking_reference", "total_price", "created_at", "updated_at")
	autocomplete_fields = ("room",)
	fieldsets = (
		(
			"Guest details",
			{
				"fields": (
					"booking_reference",
					"full_name",
					"cnic",
					"email",
					"phone_number",
					"address",
				),
				"classes": ("collapse",),
			},
		),
		(
			"Stay details",
			{
				"fields": (
					"room_type",
					"room",
					"booking_days",
					"airport_pick_drop",
					"total_price",
					"status",
					"notes",
				),
			},
		),
		(
			"Timestamps",
			{"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
		),
	)
